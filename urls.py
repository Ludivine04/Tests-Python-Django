from django.urls import path, include
#from cours.settings import AUTH_PASSWORD_VALIDATORS
from django.contrib import admin
from django.views.generic import TemplateView

from cours.views import (
    creer_enquete,
    creer_session, 
    #login_user, 
    liste_sessions, 
    modifier_session, 
    supprimer_session, 
    remplir, 
    etudiants,
    formateur, 
    redirectioncompte,
    resultat,
    CustomTokenObtainPairView   
)

urlpatterns = [   
    # Chemin admin
    path("admin/", admin.site.urls),

    # Chemin pour afficher le profil d'un formateur
    path('formateur/', formateur, name='formateur'),

    # Chemin pour afficher le profil d'un étudiant
    path('etudiants', etudiants, name='etudiants'),

    #
    path("accounts/", include('django.contrib.auth.urls')),

    # Chemin pour l'URL racine avec une vue générique comme TemplateView
    path('', TemplateView.as_view(template_name='accueil.html'), name='accueil'),

    # Redirection
    path('redirectioncompte', redirectioncompte, name='redirection'),

    # Chemin
    path('session/creer', creer_session, name='creer_session'),

    # Cehmin pour créer formulaire
    path('enquete/formulaire', creer_enquete, name='creer_formulaire'),

    # Chemin pour modifier une session de cours spécifique
    path('session/modifier/<int:session_id>', modifier_session, name='modifier_session'),

    # Chemin pour supprimer une session de cours spécifique
    path('session/supprimer/<int:session_id>', supprimer_session, name='supprimer_session'),

    # Chemin pour afficher la liste des sessions de cours existantes
    path('sessions', liste_sessions, name='liste_sessions'),

    # Chemin pour remplir un formulaire pour une session de cours spécifique
    path('enquete/remplir<int:session_id>', remplir, name='remplir'),

    # Resulats
    path('enquete/resultat', resultat, name='resultat'),

    path('api/token/', CustomTokenObtainPairView, name='token_obtain_pair'),

    


]
