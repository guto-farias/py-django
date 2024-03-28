from django.shortcuts import render
from .models import Topic

def index(request):
    """index learning_logs"""
    return render(request, 'learning_logs/index.html') #o request busca a pagina templates por padrão


def topics(request):
    """view pra topics"""
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics} #recebe um dicionario
    return render(request, 'learning_logs/topics.html', context)


def topic(request, topic_id):
    """mostra um único assunto e suas entries"""
    
    topic = Topic.objects.get(id = topic_id)
    entries = topic.entry_set.order_by('-date_added') 
    context = {'topic' : topic, 'entries' : entries}
    return render(request, 'learning_logs/topic.html', context)