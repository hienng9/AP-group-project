from django import forms
from .models import BoardGame, Loan


class BoardGameForm(forms.ModelForm):
    class Meta:
        model = BoardGame
        fields = ['name', 'description']


class LoanForm(forms.Form):
    class Meta:
        model = Loan
        fields = ['game']