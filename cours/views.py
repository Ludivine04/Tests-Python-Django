from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseBadRequest
from flask import sessions
from .models import Session, Formulaire
from .forms import SessionCoursForm, FormulaireForm
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

def accueil(request):
    return render(request, 'cours/accueil.html')

# Vue pour le profil d'un formateur
@login_required
def formateur(request):
    formateur = request.user
    sessionsutilisateur=Session.objects.filter(formateur=formateur.id)
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
    session = get_object_or_404(Session)
    if request.method == 'POST':
        form = FormulaireForm(request.POST)
        if form.is_valid():
            formulaire = form.save(commit=False)
            formulaire.session = session
            formulaire.save()
            return redirect('creer_session')
    else:
        form = FormulaireForm()
    return render(request, 'cours/enquete/remplir.html', {'form': form, 'session': session})

# Vue pour modifier les détails d'une session de cours existante
@login_required
def modifier_session(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    
    if request.method == 'POST':
        form = SessionCoursForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            return redirect('formateur')
    else:
        form = SessionCoursForm(instance=session)
    
    return render(request, 'cours/session/editer.html', {'form': form})

# Vue pour supprimer une session de cours existante
@login_required
def supprimer_session(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    if request.method == 'POST':
        session.delete() 
        return redirect('formateur')

# Vue pour afficher la liste de toutes les sessions de cours disponibles
@login_required
def liste_sessions(request,):
    sessions = Session.objects.all()
    return render(request, 'cours/liste_sessions.html', {'sessions': sessions})


# Vue pour le remplissage d'un formulaire
@login_required
def remplir(request, session_id):
    try:
        session_id = int(session_id)
    except ValueError:
        return HttpResponseBadRequest("L'ID de session n'est pas valide.")

    session_cours = get_object_or_404(Session, pk=session_id)
    
    if request.method == 'POST':
        form = FormulaireForm(request.POST)

        if form.is_valid():
            user_name = request.user.first_name
            user_lastname = request.user.last_name
            avancement_tp = form.cleaned_data.get('avancement_tp')
            difficulte = form.cleaned_data.get('difficulte')
            progression = form.cleaned_data.get('progression')

            formulaire = Formulaire(
                nom=user_name,
                prenom=user_lastname,
                session=session_cours,
                avancement_tp=avancement_tp,
                difficulte=difficulte,
                progression=progression
            )
            formulaire.save()

            return redirect(request.META.get('HTTP_REFERER', 'cours:accueil'))
    else:
        form = FormulaireForm(initial={'session_id': session_id})

    return render(request, 'cours/enquete/remplir.html', {'form': form, 'session': session_cours})


@staff_member_required
def resultat(request):
    return render(request, 'cours/enquete/resultat.html')

@login_required
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            user = self.user
            refresh = response.data.get('refresh')
            access = response.data.get('access')

            
            payload = {
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
            }

            refresh_token = RefreshToken(refresh)
            refresh_token.payload.update(payload)

            return Response({
                'access': access,
                'refresh': str(refresh_token),
            })

        return response

