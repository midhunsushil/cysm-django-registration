from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.conf import settings
import random, os, csv

#Variable

#Other functions

# Create your views here.

def game(request) :

    template_name = "chat_mon_game/chat_game.html"
    return render(request, template_name, )

def getChat(request) :

        if request.method == "POST":

            chatData = getrandomChat()
            if(chatData) :
                return JsonResponse(chatData)
            else :
                return JsonResponse({'errorExist' : True})

        return HttpResponseForbidden()

def getrandomChat() :

    path = os.path.join(settings.BASE_DIR, "media", "chat_mon_game")
    # csv file name
    filename = "chatlog.csv"
    # csv file path
    csvfilepath = os.path.join(path, filename)

    # initializing the titles and rows list
    fields = []
    rows = []
    no_of_rows = 0

    # reading csv file
    with open(csvfilepath, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)

        # extracting field names through first row
        fields = next(csvreader)

        # extracting each data row one by one
        for row in csvreader:
            rows.append(row)

        # get total number of rows
        no_of_rows = csvreader.line_num-1
        print("Total no. of chats read:", no_of_rows)

    randChat = random.randint(0,no_of_rows-1)
    print("randchat:", randChat)

    chatData = {
        'slno' : rows[randChat][0],
        'from' : rows[randChat][1],
        'chat' : rows[randChat][2],
        'moderation' : rows[randChat][3],
    }
    return chatData
