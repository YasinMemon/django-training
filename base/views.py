from django.shortcuts import render
from django.http import HttpResponse
from .models import Room

# Create your views here.

def home(request):
    rooms = Room.objects.all()
    return render(request, 'base/index.html', {'rooms': rooms})

def room(request, pk):
    room = Room.objects.get(id=pk)
    return render(request, 'base/room.html', {'room': room})
