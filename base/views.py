from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room, Topic, Message
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages




# --------------------------------- < HOME > ---------------------------------------------- 
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # return render(request, 'home.html')
    topics = Topic.objects.all()
    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))
    room_messages = Message.objects.filter(room__topic__name__icontains=q)
    room_count = rooms.count()
    context = {'rooms':rooms, 'topics':topics, 'room_count':room_count, 'room_messages':room_messages}
    return render(request, 'base/home.html', context)


# --------------------------------- < /HOME > --------------------------------------------


# --------------------------------- < ROOM > ---------------------------------------------- 
def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )

        room.participants.add(request.user)
       
        return redirect('Room-Page', pk=pk)
    context = {'room':room, 'room_messages':room_messages, 'participants':participants}
    return render(request, 'base/room.html',context)

# --------------------------------- < /ROOM > ----------------------------------------------------

# --------------------------------- < CREATE ROOM > ---------------------------------------------- 
@login_required
def create_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if(form.is_valid):
            form.save(commit=False)
            form.host = request.user
            form.save()
        return redirect('Home-Page')
    form = RoomForm()
    context = {'form':form}

    return render(request, 'base/room_form.html',context)

# --------------------------------- < /CREATE ROOM > ---------------------------------------------- 

# --------------------------------- < UPDATE ROOM > ---------------------------------------------- 
@login_required
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if(request.user != room.host):
        return HttpResponse("You are not allowed here")
    if(request.method == 'POST'):
        form = RoomForm(request.POST, instance=room)
        if(form.is_valid):
            form.save()
        return redirect('Home-Page')
    context = {'form':form}
    return render(request, 'base/room_form.html', context)
# --------------------------------- < /UPDATE ROOM > ---------------------------------------------- 

# --------------------------------- < REGISTER > ---------------------------------------------- 
def register(request):
    page = 'register'
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('Home-Page')
        else:
            messages.error(request, 'An error occured during registration')
    context = {
        'form':form,
        'page':page,
    }
    return render(request, 'base/login_register.html', context)

# --------------------------------- < /REGISTER > ---------------------------------------------- 

# --------------------------------- < DELETE MESSAGE > -----------------------------------------
def delete_message(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse("You are not authorized user ")
    if(request.method == 'POST'):
        message.delete()
        return redirect('Home-Page')
# --------------------------------- < /DELETE MESSAGE > -----------------------------------------