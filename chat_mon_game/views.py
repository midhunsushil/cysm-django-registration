from django.shortcuts import render
from django.http import HttpResponse

#Variable
global_count = 0

#Other functions

# Create your views here.

def game(request) :

    global global_count
    global_count = 0
    template_name = "chat_mon_game/chat_game.html"
    return render(request, template_name, )

def getChat(request) :

        global global_count
        global_count = global_count + 1
        return HttpResponse(global_count)
