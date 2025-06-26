from django import forms
from .models import PrediccionBonus

class PrediccionBonusForm(forms.ModelForm):
    class Meta:
        model = PrediccionBonus
        fields = ['campeon', 'goleador', 'mvp']
