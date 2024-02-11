from datetime import date
import datetime
from http.client import responses
from os import error
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.exceptions import ValidationError
from flask import sessions
from .models import Session, Formulaire
from .forms import SessionCoursForm, FormulaireForm
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

def accueil(request):
    return render(request, 'cours/accueil.html')

# Vue pour le profil d'un formateur
@login_required
def formateur(request):
    # Récupérer le formateur à partir de la requête
    formateur = request.user
    sessionsutilisateur=Session.objects.filter(formateur=formateur.id)
    # Passer les informations du formateur au modèle pour affichage
    return render(request, 'cours/utilisateurs/formateur.html', {'formateur': formateur, 'sessions': sessionsutilisateur,})

def redirectioncompte(request):
    user=request.user
    print (user.groups.all())
    if user.groups.filter(name='etudiants').exists():
        return redirect('etudiants')
    elif user.groups.filter(name='Formateurs').exists():
        return redirect('formateur')
    else:
        return ('error')
    
# Vue pour le profil d'un etudiant
@login_required
def etudiants(request):
    etudiants = request.user
    print (etudiants)
    reponses = Session.objects.all()
    return render(request, 'cours/utilisateurs/etudiants.html', {'etudiants': etudiants, 'reponses': reponses})


# Vue pour la création d'une session de cours
@login_required
def creer_session(request):
    if request.method == 'POST':
        form = SessionCoursForm(request.POST)
        # Vérifie si les données du formulaire sont valides
        if form.is_valid():
            session = form.save(commit=False)
            if session.formateur_id is None:
                session.formateur_id=request.user.id
            session.save()
            print("Session créée avec succès:", session.titre)
            return redirect('formateur')  
    else:
        form = SessionCoursForm()
    return render(request, 'cours/session/creer.html', {'form': form})


# Vue pour la création d'un formulaire associé à une session de cours spécifique
@login_required
def creer_enquete(request):
    # Récupère la session de cours associée à l'identifiant fourni, ou renvoie une erreur 404 si la session n'existe pas
    session = get_object_or_404(Session)
    if request.method == 'POST':
        # Crée une instance du formulaire de création de formulaire avec les données reçues
        form = FormulaireForm(request.POST)
        # Vérifie si les données du formulaire sont valides
        if form.is_valid():
            # Enregistre le nouveau formulaire dans la base de données en associant la session de cours correspondante
            formulaire = form.save(commit=False)
            formulaire.session = session
            formulaire.save()
            # Redirige l'utilisateur vers la page de création de session de cours après la création du formulaire
            return redirect('creer_session')
    else:
        form = FormulaireForm()
    return render(request, 'cours/enquete/remplir.html', {'form': form, 'session': session})

# Vue pour modifier les détails d'une session de cours existante
@login_required
def modifier_session(request, session_id):
    # Récupère la session de cours correspondante
    session = get_object_or_404(Session, id=session_id)
    
    if request.method == 'POST':
        # Si la méthode de la requête est POST, cela signifie que le formulaire a été soumis
        form = SessionCoursForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            # Redirection vers la page affichant la liste des sessions de cours après la modification
            return redirect('formateur')
    else:
        # Si la méthode de la requête n'est pas POST, cela signifie que la page est simplement chargée pour la première fois
        # Dans ce cas, un formulaire pré-rempli avec les détails de la session de cours existante est affiché
        form = SessionCoursForm(instance=session)
    
    return render(request, 'cours/session/editer.html', {'form': form})

# Vue pour supprimer une session de cours existante
@login_required
def supprimer_session(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    if request.method == 'POST':
        session.delete() 
        return redirect('formateur')
    
    # Si la méthode de la requête n'est pas POST, cela signifie que la page est simplement chargée pour la première fois
    # Dans ce cas, la page de confirmation de la suppression de la session est affichée
    # return render(request, 'cours/supprimer_session_cours.html', {'session': session})

# Vue pour afficher la liste de toutes les sessions de cours disponibles
@login_required
def liste_sessions(request,):
    # Récupère toutes les sessions de cours de la base de données
    sessions = Session.objects.all()
    # Renvoie la page HTML de la liste des sessions de cours avec les sessions récupérées
    return render(request, 'cours/liste_sessions.html', {'sessions': sessions})






'''
# Vue pour la connexion d'utilisateur
def login_user(request):
    # Vérifie si la méthode de requête est POST (lorsque le formulaire est soumis)
    if request.method == 'POST':
        # Crée une instance du formulaire d'authentification avec les données de la requête
        form = AuthenticationForm(request, request.POST)
        # Vérifie si les données du formulaire sont valides
        if form.is_valid():
            # Récupère le nom d'utilisateur et le mot de passe à partir du formulaire
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # Vérifie si l'utilisateur existe dans la base de données et que les informations sont correctes
            user = authenticate(username=username, password=password)
            print(user)
            userProfile=UserProfile.objects.filter(user=user.id)
            if user is not None:
                login(request, user)
                # Vérifie si l'utilisateur est un formateur avant de le rediriger
                if user.is_formateur:
                    return redirect('liste_sessions_de_cours')
                else:
                    # Redirigez l'utilisateur vers une page par défaut ou affichez un message d'erreur
                    messages.error(request, "Vous n'êtes pas autorisé à accéder à cette page.")
                    return redirect('page_non_autorisee')  # Redirige vers une page de message d'erreur
                
    else:
        # Crée une instance vide du formulaire d'authentification pour afficher le formulaire de connexion
        form = AuthenticationForm()
        # Rend la page de connexion avec le formulaire, qu'il soit valide ou vide
    return render(request, 'cours/login.html', {'form': form})

# Vue pour l'inscription d'un étudiant
class InscriptionEtudiant(APIView):
    def post(self, request):
        # Sérialise les données reçues dans la requête en utilisant EtudiantSerializer
        serializer = EtudiantSerializer(data=request.data)
        # Vérifie si les données sérialisées sont valides
        if serializer.is_valid():
            # Si les données sont valides, enregistre l'étudiant dans la base de données
            serializer.save()
            # Retourne une réponse avec les données sérialisées et le code de statut 201 (Created)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Si les données ne sont pas valides, retourne une réponse avec les erreurs de validation
            # et le code de statut 400 (Bad Request)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Fonction pour vérifier si l'utilisateur est un formateur
def is_formateur(user):
    return user.is_authenticated and user.is_staff

@login_required
def profil(request):
    # Vérifie si la méthode de la requête est POST
    if request.method == 'POST':
        # Crée un formulaire UserProfileForm avec les données soumises par l'utilisateur
        form = UserProfileForm(request.POST, instance=request.user.userprofile)
        # Vérifie si les données du formulaire sont valides
        if form.is_valid():
            # Enregistre les données mises à jour du formulaire dans la base de données
            form.save()
            # Redirige l'utilisateur vers la page de profil après la mise à jour
            return redirect('profil')
    # Si la méthode de la requête est GET
    else:
        # Crée un formulaire UserProfileForm pré-rempli avec les données du profil de l'utilisateur actuel
        form = UserProfileForm(instance=request.user.userprofile)
        # Rend la page de profil avec le formulaire approprié, prêt à être affiché
    return render(request, 'cours/profil.html', {'form': form})

    # Méthode pour mettre à jour les données du profil de l'étudiant
    def put(self, request):
        # Récupère l'utilisateur connecté (étudiant)
        etudiant = request.user
        # Sérialise les données reçues dans la requête
        serializer = EtudiantSerializer(etudiant, data=request.data)
        # Vérifie si les données sérialisées sont valides
        if serializer.is_valid():
            # Enregistre les données mises à jour du profil de l'étudiant dans la base de données
            serializer.save()
            # Retourne les données sérialisées mises à jour en tant que réponse
            return Response(serializer.data)
        # Retourne les erreurs de validation si les données sérialisées ne sont pas valides
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''

# Vue pour le remplissage d'un formulaire
@login_required
def remplir(request, session_id):
    try:
        session_id = int(session_id)
    except ValueError:
        return HttpResponseBadRequest("L'ID de session n'est pas valide.")

    #session_cours = Session.objects.get(id=session_id)
    session_cours = get_object_or_404(Session, pk=session_id)
    
    #if session_cours.date_fin > datetime.date.today():
        #return HttpResponseBadRequest("La session de cours est terminée.")

    if request.method == 'POST':
        form = FormulaireForm(request.POST)

        if form.is_valid():
            nom = form.cleaned_data.get('nom')
            print (nom)
            prenom = form.cleaned_data.get('prenom')
            print (prenom)
            avancement_tp = form.cleaned_data.get('avancement_tp')
            difficulte = form.cleaned_data.get('difficulte')
            progression = form.cleaned_data.get('progression')

            formulaire = Formulaire(session=session_cours, avancement_tp=avancement_tp, difficulte=difficulte, progression=progression)
            formulaire.save()

            
            # Redirection vers la page précédente
            return redirect(request.META.get('HTTP_REFERER', 'cours:accueil'))
    else:
        form = FormulaireForm(initial={'session_id': session_id})

    return render(request, 'cours/enquete/remplir.html', {'form': form, 'session': session_cours})
