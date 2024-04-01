from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm

def logout_view(request):
    """Faz logout de user"""
    
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    """Faz o cadastro de um novo user"""
    if request.method != 'POST':
        # exibe form em branco
        form = UserCreationForm()
    else:
        # processa form preenchido
        form = UserCreationForm(data = request.POST)
        
        if form.is_valid():
            new_user = form.save()
        # faz login e redireciona para index
            authenticated_user = authenticate(username = new_user.username, password = request.POST['password1']) #autentica user
            login(request, authenticated_user) #loga user
            return HttpResponseRedirect(reverse('index'))
        
    context = {'form' : form}
    return render(request, 'users/register.html', context)