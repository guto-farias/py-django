from django.shortcuts import render
from .models import Sell
from .forms import SellForm
from django.http import HttpResponseRedirect
from django.urls import reverse

def index(request):
    """View para index."""
    return render(request, 'seller_data/index.html') #o request busca a pagina templates por padrão


def new_sell(request):
    """View para cadastro de venda."""
    if request.method != 'POST':
        #nenhum dado submetido cria formulario em branco
        form = SellForm()
    else:
        #dados de POST submetidos, processamento
        form = SellForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index')) #usa reverse para puxar a url sem 'saber' a url, ou seja pelo name dado em urls.py (mantendo em new sell pela exigencia do trab)
        
    context = {'form': form}
    return render(request, 'seller_data/new_sell.html', context)

