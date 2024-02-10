from django import forms
from .models import Session, Formulaire

# Définition des choix pour les champs 'difficulte' et 'progression'
DIFFICULTE_CHOICES = [
    ('facile', 'Facile'),
    ('ok', 'OK'),
    ('un_peu_complique', 'Un peu compliqué'),
    ('tres_complique', 'Très compliqué'),
    ('au_secours', 'Au secours'),
]

PROGRESSION_CHOICES = [
    ('compris', 'J’ai compris'),
    ('pratiquer', 'Je dois encore pratiquer'),
    ('flou', 'C’est flou'),
]

class SessionCoursForm(forms.ModelForm):
    """
    Formulaire pour la création d'une session de cours.
    """
    class Meta:
        model = Session
        fields = ['titre', 'description', 'date_debut', 'date_fin']

class FormulaireForm(forms.ModelForm):
    """
    Formulaire pour la création d'un formulaire.
    """
    class Meta:
        model = Formulaire
        fields = ['pourcentage', 'difficulte', 'progression']
        

