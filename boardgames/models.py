from django.db import models
from django.contrib.auth.models import User


class BoardGame(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    status_choices = [
        ('A', 'Available'),
        ('B', 'Borrowed'),
    ]
    status = models.CharField(max_length=1, choices=status_choices, default='A')

    def __str__(self):
        return self.name


class Loan(models.Model):
    borrower = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(BoardGame, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.borrower.user.username} borrowed {self.game.name}"




