from django.urls import path
from . import views

app_name = 'boardgames'
urlpatterns = [
    # Home Page
    path('', views.index, name='index'),
    # Page that shows all the games
    path('all_games/', views.all_games, name='all_games'),
    # Page for adding a new boardgame
    path('new_game/', views.new_game, name='new_game'),
    # Detail page for a single boardgame
    path('all_games/<int:game_id>/', views.game_detail, name='game_detail'),
    # Page for editing a board game
    path('edit_game/<int:game_id>/', views.edit_game, name="edit_game"),
    # Page for editing a board game
    path('delete_game/<int:game_id>/', views.delete_game, name="delete_game"),
    # Page for showing user's profile
    path('profile/', views.profile, name='profile'),
    # Page for borrowing a boardgame

    path('borrow_game/<int:game_id>/', views.borrow_game, name='borrow_game'),

    path('return_game/<int:loan_id>/', views.return_game, name='return_game'),
]