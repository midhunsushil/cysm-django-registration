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

def getChats() :

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

        return [rows, no_of_rows]

def getrandomChat() :

    chats, no_of_rows = getChats()
    randChat = random.randint(0,no_of_rows-1)
    print("randchat:", randChat)

    chatData = {
        'slno' : chats[randChat][0],
        'from' : chats[randChat][1],
        'chat' : chats[randChat][2],
        'moderation' : chats[randChat][3],
    }
    return chatData

def submitTest(request):

    if request.method == "POST" :

        score_plus = 0
        score_minus = 0
        print("Printing request")
        data = request.POST
        answers = data.dict()
        chats, no_of_rows = getChats()
        print(answers)
        for key in answers :

            intKey = int(key)
            print(intKey)
            correct_answer = chats[intKey-1][3]
            answer = answers[key]
            if(correct_answer == answer) :
                score_plus = score_plus + 1
            else :
                score_minus = score_minus + 1
        json_response = {
            "status" : 1,
            "message" : "Success",
            "score_plus" : score_plus,
            "score_minus" : score_minus,
        }
        return JsonResponse(json_response)

def submitTestResponse(request, score_plus, score_minus):

    template_name = "chat_mon_game/test_submitted.html"
    context = { "score_plus" : score_plus, "score_minus" : score_minus }
    return render(request, template_name, context)
