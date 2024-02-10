from django.db import models
from django.contrib.auth.models import User

class Session(models.Model):
    titre = models.CharField(max_length=100)
    description = models.TextField()
    statut = models.CharField(max_length=10, choices=[('ouvert', 'Ouvert'), ('ferme', 'Fermé')])
    date_debut = models.DateField()
    date_fin = models.DateField()
    formateur = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titre
    
class Formulaire(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    pourcentage = models.IntegerField()
    difficulte = models.CharField(max_length=100)
    progression = models.CharField(max_length=100)
    premiereconnexion = models.DateTimeField()
    derniereconnexion = models.DateTimeField()

    def __str__(self):
        return f"Formulaire pour {self.session.titre}"
