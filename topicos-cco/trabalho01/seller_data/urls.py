from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'), 
    path('new_sell', views.new_sell, name = 'new_sell'),
]