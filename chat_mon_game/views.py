from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.conf import settings
import random, os, csv

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

        if request.method == "POST":
            global global_count
            global_count = global_count + 1
            return HttpResponse(getrandomChat())

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
    return rows[randChat][2]
