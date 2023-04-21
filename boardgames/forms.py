from django import forms
from .models import BoardGame, Loan


class BoardGameForm(forms.ModelForm):
    class Meta:
        model = BoardGame
        fields = ['name', 'age_range', 'description']


class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = []