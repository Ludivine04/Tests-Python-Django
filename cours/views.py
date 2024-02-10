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
    formateur = request.user  # Supposant que le formateur est stocké en tant qu'utilisateur dans le système d'authentification
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
    
# Vue pour le profil d'un formateur
@login_required
def etudiants(request):
    # Récupérer le formateur à partir de la requête
    etudiants = request.user  # Supposant que le formateur est stocké en tant qu'utilisateur dans le système d'authentification

    # Passer les informations du formateur au modèle pour affichage
    return render(request, 'cours/utilsateurs/etudiants.html', {'etudiants': etudiants})


# Vue pour la création d'une session de cours
@login_required
def creer_session(request):
    # Vérifie si la requête est une méthode POST (envoi de données)
    if request.method == 'POST':
        # Crée une instance du formulaire de création de session de cours avec les données reçues
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
        # Si la requête n'est pas de type POST, crée une instance vide du formulaire de création de session de cours
        form = SessionCoursForm()
    # Renvoie la page HTML du formulaire de création de session de cours avec le formulaire et les sessions existantes
    return render(request, 'cours/session/creer.html', {'form': form})


# Vue pour la création d'un formulaire associé à une session de cours spécifique
@login_required
def creer_enquete(request):
    # Récupère la session de cours associée à l'identifiant fourni, ou renvoie une erreur 404 si la session n'existe pas
    session = get_object_or_404(Session)
    # Vérifie si la requête est une méthode POST (envoi de données)
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
        # Si la requête n'est pas de type POST, crée une instance vide du formulaire de création de formulaire
        form = FormulaireForm()
    # Renvoie la page HTML du formulaire de création de formulaire avec le formulaire et la session de cours associée
    return render(request, 'cours/enquete/avancement.html', {'form': form, 'session': session})

# Vue pour modifier les détails d'une session de cours existante
@login_required
def modifier_session(request, session_id):
    # Récupère la session de cours correspondante
    session = get_object_or_404(Session, id=session_id)
    
    if request.method == 'POST':
        # Si la méthode de la requête est POST, cela signifie que le formulaire a été soumis
        form = SessionCoursForm(request.POST, instance=session)
        if form.is_valid():
            # Si le formulaire est valide, les modifications sont enregistrées dans la base de données
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
# Vue pour le profil d'un étudiant
@login_required
class ProfilEtudiant(APIView):
    # Méthode pour récupérer les données du profil de l'étudiant
    def get(self, request):
        # Récupère l'utilisateur connecté (étudiant)
        etudiant = request.user
        # Sérialise les données de l'étudiant
        serializer = EtudiantSerializer(etudiant)
        # Retourne les données sérialisées en tant que réponse
        return Response(serializer.data)
'''

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


# Vue pour la connexion d'un étudiant
@login_required
class ConnexionEtudiant(APIView):
    # Récupère le nom d'utilisateur et le mot de passe à partir des données de la requête POST
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        # Recherche l'étudiant correspondant dans la base de données par son nom d'utilisateur
        etudiant = Etudiant.objects.filter(username=username).first()
        # Vérifie si l'étudiant existe et si le mot de passe fourni est correct
        if etudiant and etudiant.check_password(password):
            # Génère un nouveau jeton d'actualisation (refresh token) pour l'étudiant
            refresh = RefreshToken.for_user(etudiant)
            # Retourne une réponse avec le jeton d'actualisation et le jeton d'accès (access token)
            return Response({'refresh': str(refresh), 'access': str(refresh.access_token)})
        # Si l'étudiant n'existe pas ou si le mot de passe est incorrect, retourne une réponse d'erreur
        # avec un message approprié et le code de statut 401 (Unauthorized)
        return Response({'error': 'Nom d\'utilisateur ou mot de passe incorrect'}, status=status.HTTP_401_UNAUTHORIZED)




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

    
# Vue pour le remplissage d'un formulaire
@login_required
def remplir_formulaire(request, session_id):
    # Récupérer la session de cours correspondant à l'identifiant fourni
    session_cours = get_object_or_404(SessionCours, pk=session_id)
    try:
        # Assurez-vous que l'ID de session est un entier
        session_id = int(session_id)
    except ValueError:
        # Si l'ID de session n'est pas un entier valide, renvoyer une réponse BadRequest
        return HttpResponseBadRequest("L'ID de session n'est pas valide.")

    # Récupérer la session de cours correspondant à l'identifiant fourni
    try:
        session_cours = SessionCours.objects.get(pk=session_id)
    except SessionCours.DoesNotExist:
        # Si aucune session de cours correspondante n'est trouvée, renvoyer une réponse BadRequest
        return HttpResponseBadRequest("La session de cours spécifiée n'existe pas.")
    
    # Vérifie si c'est la première connexion de l'utilisateur dans la session
    if 'premiere_connexion' not in request.session:
        # Enregistre la date et l'heure de la première connexion de l'utilisateur dans la session
        request.session['premiere_connexion'] = timezone.now()
        # Exemple d'utilisation de ValidationError pour une validation personnalisée

    if session_cours.date_fin < timezone.now():
        raise ValidationError("La session de cours est terminée.")
        # Récupérez la session de cours correspondant à l'identifiant fourni
        session_cours = get_object_or_404(SessionCours, pk=session_id)
        # Si la méthode de la requête est POST, cela signifie que l'utilisateur a soumis le formulaire
    
    if request.method == 'POST':
        # Créez une instance de FormulaireEtudiant avec les données soumises par l'utilisateur
        form = FormulaireEtudiant(request.POST)

        # Vérifie si les données soumises sont valides
        if form.is_valid():
            # Récupérer l'ID de session à partir des données soumises
            session_id = form.cleaned_data['session_id']
            # Récupérer la session de cours correspondant à l'identifiant fourni
            session_cours = get_object_or_404(SessionCours, pk=session_id)

            # Si le formulaire est valide, vous pouvez accéder aux données soumises
            nom = form.cleaned_data['nom']
            prenom = form.cleaned_data['prenom']
            print("Nom soumis dans le formulaire :", nom)
            print("Prénom soumis dans le formulaire :", prenom)
            avancement_tp = form.cleaned_data['avancement_tp']
            difficulte = form.cleaned_data['difficulte']
            progression = form.cleaned_data['progression']

             # Récupère l'identifiant de session à partir des données soumises (si disponible)
            session_id = form.cleaned_data['session_id']
            # Récupère la session de cours correspondant à l'identifiant fourni
            session_cours = get_object_or_404(SessionCours, pk=session_id)
            session_cours = SessionCours.objects.get(id=session_id)
            # Créez un objet Formulaire avec les données du formulaire et l'identifiant de session
            formulaire = Formulaire(session=session_cours, avancement_tp=avancement_tp, difficulte=difficulte, progression=progression)
            formulaire.save()

            # Utilisation d'une transaction pour garantir l'intégrité des données dans la base de données
            with transaction.atomic():
                formulaire = Formulaire.objects.create(
                    session=session_cours,
                    nom=nom,
                    prenom=prenom,
                    avancement_tp=avancement_tp,
                    difficulte=difficulte,
                    progression=progression
                )

            # Redirection vers une page de confirmation
            return HttpResponse("Formulaire soumis avec succès !")

    else:
        # Créer le formulaire avec ou sans données initiales
        form = FormulaireEtudiant(initial={'session_id': session_id})

    # Passez l'objet session à votre template pour pouvoir accéder à son ID
    return render(request, 'cours/remplir_formulaire.html', {'form': form, 'session': session_cours})
'''