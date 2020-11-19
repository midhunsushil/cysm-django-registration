from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.conf import settings
from chat_mon_game.forms import *
import random, os, csv, datetime

#Variable

#Other functions

# Create your views here.

def test_reg(request) :

    template_name = "chat_mon_game/chat_test_reg.html"
    form = User_Reg()
    if request.method == "GET" and request.session.get("test_started", False) :
        return redirect("Test")
    if request.method == "POST" :
        form = User_Reg(request.POST)
        if form.is_valid() :
            print("Form Valid")
            request.session['name'] = form.cleaned_data['name']
            request.session['email'] = form.cleaned_data['email']
            request.session['visited_reg_page'] = True
            return redirect("Test")
    context = {"form" : form}
    return render(request, template_name, context)

def game(request) :

    test_time_min = 2
    if request.method == "POST" :
        print("answers", request.session.get("answers", False))
        if request.session.get("answers", False) :
            return JsonResponse(request.session.get("answers"))
        else :
            return JsonResponse({'errorExist' : True})

    print("test sessions")
    print(request.session.get('visited_reg_page'))
    if (request.session.get('visited_reg_page', False)) :
        # request.session['visited_reg_page'] = False

        if request.session.get('test_started', False) == False :
            test_end_time = datetime.datetime.now() + datetime.timedelta(minutes = test_time_min)
            request.session['test_end_time'] = test_end_time

        time_left = request.session['test_end_time'] - datetime.datetime.now()
        time_left_seconds = int(time_left.total_seconds())
        print("Time Left:", time_left_seconds)

        request.session['test_started'] = True
        template_name = "chat_mon_game/chat_game.html"
        context = {"time_left" : time_left_seconds}
        return render(request, template_name, context)
    else :
        return HttpResponseForbidden()

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

def updateAnswer(request) :

    if request.method == "POST" :

        data = request.POST
        request.session['answers'] = data
        print("ANswers: ", data)
        if data :
            return HttpResponse("Success")
        else :
            return HttpResponse("Failed")

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
            correct_answer = chats[intKey-1][3].lower()
            answer = answers[key].lower()
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
    request.session.flush()
    return render(request, template_name, context)
