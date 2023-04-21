from datetime import timezone

from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import BoardGameForm, LoanForm
from .models import BoardGame, Loan

def index(request):
    return render(request, 'boardgames/index.html')


def all_games(request):
    """Show all board games."""
    games = BoardGame.objects.all()
    borrowed_games = []
    # if the user is authenticated then do not show the game that is borrowed by him/her
    if request.user.is_authenticated:
        loans = Loan.objects.filter(Q(borrower=request.user) & Q(is_returned = False))
        borrowed_games = [loan.game for loan in loans]

    context = {'games': games, 'borrowed_games': borrowed_games}
    return render(request, 'boardgames/all_games.html', context)


def game_detail(request, game_id):
    """Show information of a boardgame."""
    game = BoardGame.objects.get(id=game_id)
    current_loan = None
    if not game.is_available:
        loan = Loan.objects.filter(Q(game = game) & Q(is_returned = False))
        current_loan = loan[0]
        print(current_loan.borrow_date)
  
    context = {'game': game, "current_loan": current_loan}
    return render(request, 'boardgames/game_detail.html', context)

@login_required
def edit_game(request, game_id):
    """Edit an existing boardgame."""
    game = BoardGame.objects.get(id=game_id)
    # Making sure the game belongs to the current user:
    if game.owner != request.user:
        return HttpResponse("Sorry, only the owner can edit this game")
    if request.method != 'POST':
        # Initial request, pre-fill form with the current experience.
        form = BoardGameForm(instance=game)
    else:
        # POST data submitted -> process the data.
        form = BoardGameForm(instance=game, data=request.POST)
        if form.is_valid():
            form.save()
            # Owner information is already stored.
            # edit_game.owner = request.user
            # edit_game.save()
            return redirect('boardgames:game_detail', game_id=game.id)
    context = {'game': game, 'form': form}
    return render(request, 'boardgames/edit_game.html', context)

@login_required
def delete_game(request, game_id):
    """Delete an existing boardgame."""
    game = BoardGame.objects.get(id=game_id)
    # Making sure the game belongs to the current user:
    if game.owner != request.user:
        return HttpResponse("Sorry, only the owner can delete this game")
    else:
        game.delete()
    return redirect('boardgames:all_games')


@login_required
def new_game(request):
    """Add a new game."""
    if request.method != 'POST':
        # No data submitted -> create a blank form.
        form = BoardGameForm()
    else:
        # Post data submitted -> process the data.
        form = BoardGameForm(data=request.POST)
        
        if form.is_valid():
            new_game = form.save(commit=False)  # Save topic in a variable.
            new_game.owner = request.user  # Set topics owner attribute to current user.
            new_game.save()  # Save the changes to the database.
            return redirect('boardgames:all_games')
    # Display a blank or an invalid form:
    context = {'form': form}
    return render(request, 'boardgames/new_game.html', context)

@login_required
def profile(request):
    """Show information on user's owned boardgames and their loans."""
    games = BoardGame.objects.filter(owner=request.user).all()
    loans = Loan.objects.filter(Q(borrower=request.user) & Q(is_returned = False))
    
    context = {'games': games,'loans': loans}
    return render(request, 'boardgames/profile.html', context)

@login_required
def borrow_game(request, game_id):
    """This function let user borrow new game if they are not currently borrow 3 games."""
    number_of_loans = Loan.objects.filter(Q(borrower = request.user) & Q(is_returned = False))
    game = BoardGame.objects.get(id = game_id)
    # If they have already 3 games in their loans, then show the message.
    if len(number_of_loans) >= 3:
        return HttpResponse("Sorry, you cannot borrow more than 3 games. Please return one and rety again")
    
    if request.method != 'POST':
        form = LoanForm()
    else:
        form = LoanForm(data = request.POST)
        game_form = BoardGameForm(instance=game)
        if form.is_valid():
            # Once user submit the valid loan form, game and borrower will be added to the form.
            new_entry = form.save(commit = False)
            new_entry.game = game
            new_entry.borrower = request.user
            new_entry.save()
            # Change the availability status to False, show that other people can not borrow it.
            game_form2 = game_form.save(commit=False)
            game_form2.is_available = False
            game_form2.save()
            print(game.is_available)
            return redirect('boardgames:profile')
    context = {"form": form, 'game': game}
    return render(request, 'boardgames/borrow_form.html', context)
    