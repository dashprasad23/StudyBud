from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Room, Topic
from .forms import RoomForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
            
        except:
            messages.error(request, "User doesn't  exist")
            return redirect(home)
        
        user = authenticate(request, username=username, password=password)
        print(user.is_authenticated)
        if user.is_authenticated:
            login(request, user)
            return redirect(home)
        else:
            messages.error(request, "Username OR password does't exist")
           
    context= {}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    
    logout(request)
    
    return redirect('home')

def home(request):
    q = request.GET.get('q')
    if q:
        rooms_data = Room.objects.filter(
            Q(topic__name__icontains=q) | 
            Q(name__icontains=q) | 
            Q(description__icontains=q))
    else :
        rooms_data = Room.objects.all()
    
    topics_data = Topic.objects.all()
    context = {'rooms': rooms_data, 'room_count': rooms_data.count() ,'topics': topics_data}
    #print(context)
    return render(request, 'base/home.html', context)


def room(request, pk):
    room_detail = Room.objects.get(id=pk)
    return render(request, 'base/rooms.html', {'room': room_detail})


@login_required(login_url="login")
def createRoom(request):
    context = {'form': RoomForm}
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')


    return render(request, 'base/room_form.html', context)


@login_required(login_url="login")
def updateRoom(request, pk):

    room = Room.objects.get(id=pk)

    context = {'form': RoomForm(instance=room)}
    
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
            

    return render(request, 'base/room_form.html', context)

@login_required(login_url="login")
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})


