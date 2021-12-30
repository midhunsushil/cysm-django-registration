from django.apps import AppConfig
from joblib import load
from sklearn.feature_extraction.text import TfidfVectorizer
import os

from .ml import load_model, get_vectorizer

class PredictorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'predictor'
    APP_DIR = os.path.dirname(os.path.abspath(__file__))
    datafile = os.path.join(os.path.join(APP_DIR, 'models'), 'tweet_data.csv')
    modelfile = os.path.join(os.path.join(APP_DIR, 'models'), 'model_lr_tf.pkl')
    vectorizer = get_vectorizer(datafile)
    model = load_model(modelfile)
