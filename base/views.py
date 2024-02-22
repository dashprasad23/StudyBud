from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Room, Topic
from .forms import RoomForm


def loginPage(request):
    if request.method == 'POST':
        email = request.method.POST.get('email')
        password = request.method.POST.get('password')
        print(email, password)
    context= {}
    return render(request, 'base/login_register.html', context)

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


def createRoom(request):
    context = {'form': RoomForm}
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')


    return render(request, 'base/room_form.html', context)


def updateRoom(request, pk):

    room = Room.objects.get(id=pk)

    context = {'form': RoomForm(instance=room)}
    
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
            

    return render(request, 'base/room_form.html', context)


def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})


