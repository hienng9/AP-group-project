from datetime import timezone

from django.http import Http404
from django.shortcuts import render, redirect

from .forms import BoardGameForm
from .models import BoardGame, Loan


def index(request):
    return render(request, 'boardgames/index.html')


def all_games(request):
    """Show all board games."""
    games = BoardGame.objects.order_by('-status')
    context = {'games': games}
    return render(request, 'boardgames/all_games.html', context)


def game_detail(request, game_id):
    """Show information of a boardgame."""
    game = BoardGame.objects.get(id=game_id)
    context = {'game': game}
    return render(request, 'boardgames/game_detail.html', context)


def edit_game(request, game_id):
    """Edit an existing boardgame."""
    game = BoardGame.objects.get(id=game_id)
    # Making sure the game belongs to the current user:
    if game.owner != request.user:
        raise Http404("Sorry, only the owner can edit this game")
    if request.method != 'POST':
        # Initial request, pre-fill form with the current experience.
        form = BoardGameForm(instance=game)
    else:
        # POST data submitted -> process the data.
        form = BoardGameForm(instance=game, data=request.POST)
        if form.is_valid():
            edit_game = form.save(commit=False)
            edit_game.owner = request.user
            edit_game.save()
            return redirect('boardgames:game_detail', game_id=game.id)
    context = {'game': game, 'form': form}
    return render(request, 'boardgames/edit_game.html', context)


def delete_game(request, game_id):
    """Delete an existing boardgame."""
    game = BoardGame.objects.get(id=game_id)
    # Making sure the game belongs to the current user:
    if game.owner != request.user:
        raise Http404("Sorry, only the owner can delete this game")
    else:
        game.delete()
    return redirect('boardgames:all_games')


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


def profile(request):
    """Show information on user's owned boardgames and their loans."""
    games = BoardGame.objects.filter(owner=request.user).all()
    loans = Loan.objects.filter(borrower=request.user).order_by('borrow_date')
    context = {'games': games, 'loans': loans}
    return render(request, 'boardgames/profile.html', context)