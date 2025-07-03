from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse

from .forms import RoomForm, UserForm

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from .models import Room, Topic, Message

# Create your views here.

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username OR password does not exist")

    context = {'page': page}
    return render(request, "base/login_register.html", context)

def registerUser(request):
    page = 'register'
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data.get('username').lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error occurred during registration")

    context = {'page': page, 'form' : form}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) |
                                Q(name__icontains=q) |
                                Q(description__icontains=q))
    topics = Topic.objects.all()
    room_count = rooms.count()
    msgs = Message.objects.all().order_by('-created')
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'msgs': msgs}
    return render(request, 'base/index.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    msgs = room.message_set.all().order_by('-created')
    participants = room.participants.all()

    if request.method == 'POST':
        Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('message')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'msgs': msgs, 'participants': participants}
    return render(request, 'base/room.html', context)

@login_required(login_url='login')
def delete_msg(request, pk):
    msg = Message.objects.get(id=pk)

    if request.user != msg.user:
        return HttpResponse("You are not allowed here!")

    if request.method == 'POST':
        msg.delete()
        return redirect('room', pk=msg.room.id)
    return render(request, 'base/delete.html', {'obj': msg})

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            messages.success(request, "Room created successfully! 🎉")
            return redirect('home') 
    context = {'form': form}
    return  render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("You are not allowed here!")

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("You are not allowed here!")

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})

def userProfile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_msgs = user.message_set.all()
    topics = Topic.objects.all()
    context = {"user": user, "rooms":rooms, "room_msgs": room_msgs, "topics": topics, "msgs":room_msgs }
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def updateProfile(request):
    user = request.user
    form = UserForm(instance=user)
    
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("profile", pk=user.id)

    context = {"form" : form}
    return render(request, "base/update_profile.html", context)