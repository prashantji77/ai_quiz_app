import requests
from django.shortcuts import render


def index(request): 
    return render(request, 'quiz/index.html') 
def home(request): 
    return render(request, 'quiz/home.html')