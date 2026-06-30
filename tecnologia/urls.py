from django.urls import path  
from . import views
from django.contrib import messages


urlpatterns = [
    path('', views.inicio),

]
