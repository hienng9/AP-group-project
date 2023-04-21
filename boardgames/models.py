from django.db import models
from django.contrib.auth.models import User


class BoardGame(models.Model):
    name = models.CharField(max_length=255)
    age_range = models.CharField(blank=True, null=True, max_length= 200)
    description = models.TextField()

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    status_choices = [
        (True, 'Available'),
        (False, 'Borrowed'),
    ]
    is_available = models.BooleanField('Is Available', choices=status_choices, default=True)

    # date and time of creation - required in the task
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    # date and time of modification- required in the task
    date_modified = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        ordering = ['-is_available','-date_modified', '-date_created']

    def __str__(self):
        return self.name


class Loan(models.Model):
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    game = models.ForeignKey(BoardGame, on_delete=models.CASCADE)

    borrow_date = models.DateTimeField(auto_now_add=True)

    return_date = models.DateTimeField(blank=True, null=True)
    # is retruned is added so that it is easier to do the query
    is_returned = models.BooleanField('Is returned', default = False)

    def __str__(self):
        # In case it is available
        if self.game.is_available:
            return (f"{self.game.name} is available")
        else: # If it's not available, then give 
            return (f"{self.game.name} is borrowed by {self.borrower.username} on {self.borrow_date}")




