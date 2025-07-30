from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Room, Topic, Message
from django.http import HttpResponse
from .forms import RoomForm, UserForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q

# Create your views here.

rooms = [
    {'id':'1', 'name': 'Lets learn python'},
    {'id':'2', 'name': 'Lets learn js'},
]
# @login_required(login_url="login")
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # filter to case insensitive with name completion
    rooms = Room.objects.filter(Q(topic__name__icontains = q) |
                                Q(name__icontains = q) |
                                Q(description__icontains = q)
                                )
    topics = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {
        'rooms': rooms,
        'topics':topics,
        'room_count': room_count,
        'room_messages': room_messages,
    }
    return render(request, "chat/Home.html", context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    #querying many to one rel
    room_messages = room.message_set.all()  #.order_by('-created')
    #querying many to many 
    participants = room.participants.all()
    if request.method == 'POST':
        room_messages = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect("zchatroom", pk = room.id)
    # for i in rooms:
    #     if i['id'] == int(pk):
    #         room = i
    context = {
        "room": room,
        'room_messages': room_messages,
        'participants': participants,
    }
    return render(request, "zchat/zchatRoom.html", context)
# @login_required(login_url="login")
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    # processing form data
    
    context =  {
        'topics': topics,
        'form':form
    }
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host = request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        # form = RoomForm(request.POST)
        # if form.is_valid:
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()
        return redirect('zchathome')
    else:
        return render(request, "zchat/room_form.html", context)
# @login_required(login_url="login")
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()


    context = {
        'form': form,
        'topics':topics,
        'room': room,
    }
    if request.user != room.host:
        messages.warning(request, "You can`t edit others chat !")    
        return redirect("zchathome")    
    elif request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        # if form.is_valid():
        #     form.save()
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        room.name= request.POST.get('name')
        room.topic= topic
        room.description= request.POST.get('description')
        room.save()
        return redirect('zchathome')

    else:
        return render(request, "zchat/room_form.html", context)
# @login_required(login_url="login")
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    context = {
        'obj': room
    }
    if request.user != room.host:
        messages.warning(request, "You can`t delete others chat !")    
        return redirect("zchathome")

    elif request.method == 'POST':
        room.delete()
        return redirect("zchathome")
    else:
        return render(request, "zchat/delete.html", context)
    
# @login_required(login_url="login")
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    context = {
        'obj': message
    }
    if request.user != message.user:
        messages.warning(request, "You can`t delete others chat !")    
        return redirect("zchathome")

    elif request.method == 'POST':
        message.delete()
        messages.success(request, "Message deleted successfully ! ")
        return redirect("zchathome")
    else:
        return render(request, "zchat/delete.html", context)
    
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {
        'user': user,
        'rooms': rooms,
        'room_messages': room_messages,
        'topics': topics,

    }
    return render(request, "zchat/profile.html", context)

# @login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    context = {
        'form': form,
    }
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("user-profile", pk=user.id)
    return render(request, "zchat/update_user.html", context)