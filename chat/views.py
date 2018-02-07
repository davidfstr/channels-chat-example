from django.shortcuts import render
import json


def index(request):
    return render(request, 'chat/index.html', {})


def room(request, room_name: str):
    return render(request, 'chat/room.html', {
        'room_name_json': json.dumps(room_name)
    })
