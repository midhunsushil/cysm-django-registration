from django.shortcuts import render
from rest_framework.views import APIView
from .apps import PredictorConfig
from django.http import JsonResponse
from django.http import HttpResponse

# Imports for sentiment analysis
from .ml import process_tweet
# import re
# import emoji
# import contractions
# import nltk
# from nltk.tokenize import word_tokenize
# nltk.download('punkt')
# from nltk.corpus import stopwords
# nltk.download('stopwords')
# from nltk.stem.snowball import SnowballStemmer
# import string

# Create your views here.

class Sentiment_predict(APIView):
    #permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        processed_tweet = process_tweet(request.GET.get("tweet"))
        #print(processed_tweet)
        model = PredictorConfig.model
        vectorizer = PredictorConfig.vectorizer
        transformed_tweet = vectorizer.transform([processed_tweet])
        #print(transformed_tweet)
        prediction = model.predict(transformed_tweet)
        proba = model.predict_proba(transformed_tweet)
        pos_prob =  str(round(proba[:,1].item(0), 3))
        neg_prob =  str(round(proba[:,0].item(0), 3))
        print(prediction.item(0))
        sentiment = {
            "prediction" : prediction.item(0),
            "pos_prob" : pos_prob,
            "neg_prob" : neg_prob
        }
        return JsonResponse(sentiment)
        # return HttpResponse("HI " + pos_prob)
