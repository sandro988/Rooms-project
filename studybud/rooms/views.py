from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Room, Topic, Message
from django.contrib.auth.models import User
from django.db.models import Q
from .forms import RoomForm, UserForm

# Create your views here.

def loginPage(request):
    page='login-page'

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Usename or passoword is incorrect')


        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'User does not exits')

    context = {'page': page}
    return render(request, 'rooms/login_register.html', context)

def logoutPage(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    page='register-page'
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error('Something went wrong')

    context = {'form': form, 'page': page} 
    return render(request, 'rooms/login_register.html', context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''

    rooms = Room.objects.filter(
        Q(name__icontains=q) |
        # Q(description__icontains=q) |
        Q(topic__name__icontains=q)
        ) 

    topics = Topic.objects.all()
    
    room_count = rooms.count()
    activities = Message.objects.filter(
        Q(room__topic__name__icontains=q)
        ) 

    context = {
        'rooms': rooms, 
        'topics': topics, 
        'room_count': room_count,
        'activities': activities}

    return render(request, 'rooms/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    comments = room.message_set.all()
    participants = room.participants.all()


    if request.method == 'POST':
        comment = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body'))
        messages.success(request, 'Your comment was successfully Added')
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'comments': comments, 'participants': participants}
    return render(request, 'rooms/room.html', context)

@login_required(login_url='login')
def editMessage(request, pk):
    page='edit-message'
    comment = Message.objects.get(id=pk)
    room = Room.objects.get(id=comment.room.id)
    comments = room.message_set.all()

    if request.user != comment.user:
        messages.error(request, 'You are not allowed to edit other users messages')
        return redirect('room', pk=comment.room.id)

    if request.method == 'POST':
        comment.body = request.POST.get('body')
        comment.save()
        messages.success(request, 'Your comment was successfully edited')
        return redirect('room', pk=comment.room.id)

    context = {'comment_exact': comment, 'comments': comments, 'page': page, 'room': room}
    return render(request, 'rooms/room.html', context)

@login_required(login_url='login')
def deleteMessage(request, pk):
    page='delete-message'
    comment = Message.objects.get(id=pk)

    if request.user != comment.user:
        messages.error(request, 'You are not allowed to delete other users messages')
        return redirect('room', pk=comment.room.id)

    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Your comment was successfully deleted')
        return redirect('room', pk=comment.room.id)
    context = {'obj': comment, 'page': page}
    return render(request, 'rooms/delete.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_count = rooms.count()
    activities = user.message_set.all()
    topics = Topic.objects.all()
    context = {
        'user': user, 
        'rooms': rooms, 
        'activities': activities,
        'topics': topics,
        'room_count': room_count}
    return render(request, 'rooms/profile.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    room = Room.objects.all()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        print(request.user)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('home')
        else:
            messages.error(request, 'Form is not valid')


    context = {'form': form, 'room': room}
    return render(request, 'rooms/create_edit.html', context)

@login_required(login_url='login')
def editRoom(request, pk):
    page = 'edit-room'
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        messages.error(request, 'You are not allowed to edit other users rooms')
        return redirect('home')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            messages.error(request, 'something went wrong')
        

    context = {'form': form, 'room': room, 'page': page}
    return render(request, 'rooms/create_edit.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    page='delete-room'
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        messages.error(request, 'You are not allowed to delete other users rooms')
        return redirect('home')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'obj': room, 'page': page}
    return render(request, 'rooms/delete.html', context)


@login_required(login_url='login')
def editUser(request, pk):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    context = {'form': form}
    return render(request, 'rooms/edit-user.html', context)