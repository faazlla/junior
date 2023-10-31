from django.shortcuts import get_object_or_404, render, redirect
from .models import Junior, Ocjena, Language
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from .forms import SearchForm
from .forms import JuniorRegistrationForm

def index(request):
    form = SearchForm(request.GET)
    juniori = Junior.objects.all().order_by('-prosjecna_ocjena')

    if form.is_valid():
        jezik = form.cleaned_data['Language']
        ocjena = form.cleaned_data['Rating']
        num_ocjena = form.cleaned_data['NumRatings']
        if num_ocjena:
            juniori = Junior.objects.filter(primarni_jezik=jezik, prosjecna_ocjena__gte=ocjena, broj_ocjena__gte=num_ocjena).order_by('-prosjecna_ocjena')
        else:
            juniori = Junior.objects.filter(primarni_jezik=jezik, prosjecna_ocjena__gte=ocjena).order_by('-prosjecna_ocjena')

    return render(request, 'index.html', {'juniori': juniori, 'form': form})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Junior, Ocjena
from .forms import JuniorRegistrationForm

def details(request, id):
    junior = get_object_or_404(Junior, id=id)
    ocjene = Ocjena.objects.filter(ocijenjeni_junior=junior)
    return render(request, 'details.html', {'junior': junior, 'ocjene': ocjene})


from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .forms import OcjenaForm

def rate_junior(request, id):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'User not authenticated'})

    junior = get_object_or_404(Junior, id=id)
    ocjena = Ocjena.objects.filter(ocjenjivac=request.user, ocijenjeni_junior=junior).first()
    
    if request.method == 'POST':
        form = OcjenaForm(request.POST)
        if form.is_valid():
            ocjena_vrijednost = form.cleaned_data['ocjena']
            if ocjena:
                ocjena.ocjena = ocjena_vrijednost
                ocjena.save()
            else:
                ocjena = Ocjena.objects.create(
                    ocjenjivac=request.user,
                    ocijenjeni_junior=junior,
                    ocjena=ocjena_vrijednost
                )
            ocjena.ocijenjeni_junior.calculate_average_rating()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = OcjenaForm()

    return render(request, 'rate_junior.html', {'form': form, 'junior': junior})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
		
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return redirect('index')
    else:
        return render(request, 'login.html', {})
    
def logout_user(request):
    logout(request)
    return redirect('index')


def joinus(request):
    languages = Language.objects.all()  # Pretpostavljajući da imate model Language sa atributom 'name' koji predstavlja naziv jezika
    existing_junior = Junior.objects.filter(user=request.user).first()  # Provjerite postoji li već kreiran junior profil za trenutnog korisnika

    if request.method == 'POST':
        form = JuniorRegistrationForm(request.POST, request.FILES, instance=existing_junior)
        if form.is_valid():
            junior = form.save(commit=False)
            junior.user = request.user  # Dodajte trenutnog korisnika kao vlasnika junior profila
            junior.save()
            return redirect('index')
    else:
        form = JuniorRegistrationForm(instance=existing_junior)

    return render(request, 'joinus.html', {'form': form, 'languages': languages, 'existing_junior': existing_junior})


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})
        
    return render(request, 'register.html', {'form':form})
