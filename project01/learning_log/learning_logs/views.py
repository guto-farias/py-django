from django.shortcuts import render
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required #decorators são formas simples de alterar comportamentos de funçoes sem alterar o código

def index(request):
    """index learning_logs"""
    return render(request, 'learning_logs/index.html') #o request busca a pagina templates por padrão


@login_required
def topics(request):
    """view pra topics"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics} #recebe um dicionario
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """mostra um único assunto e suas entries"""
    
    topic = Topic.objects.get(id = topic_id)
    
    #garante que assunto pertence a user atual
    if topic.owner != request.user:
        raise Http404
    
    entries = topic.entry_set.order_by('-date_added') 
    context = {'topic' : topic, 'entries' : entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """add um novo assunto"""
    if request.method != 'POST':
        #nenhum dado submetido cria formulario em branco
        form = TopicForm()
    else:
        #dados de POST submetidos, processamento
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit = False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('topics')) #usa reverse para puxar a url sem 'saber' a url, ou seja pelo name dado em urls.py
        
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """add nova entrada para o assunto especifico"""
    topic = Topic.objects.get(id = topic_id)#foreign key
    
    #garante que assunto pertence a user atual
    if topic.owner != request.user:
        raise Http404
    
    if request.method != 'POST':
        # se é diferente de post: nenhum dado submetido cria formulario em branco
        form = EntryForm()
    else:
        #dados de POST submetidos, processamento
        form = EntryForm(data = request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)#new entry vira um objeto com os dados do form, "esperando pra ser commitado"
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('topic', args=[topic_id]))
    
    context = {'topic':topic, 'form':form}
    return render(request, 'learning_logs/new_entry.html', context)
            
@login_required
def edit_entry(request, entry_id):
    """edita anotação/entrada"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    
    #garante que assunto pertence a user atual
    if topic.owner != request.user:
        raise Http404
    
    if request.method != 'POST':
        #requisição inicial; preenche form com entrada atual
        form = EntryForm(instance=entry)
        
        
    else: 
        #dados de post submetidos; processa
        form = EntryForm(instance = entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topic', args=[topic.id])) #esse args pode ser visto nas urls
        
    
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
            