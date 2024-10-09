from fastapi import FastAPI
import numpy as np
import pandas as pd
from sklearn.preprocessing import FunctionTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import scipy.sparse as sp
import os
from nltk.tokenize import word_tokenize
import pytesseract
import requests
from PIL import Image
from io import BytesIO


# Function to preprocess text
def preprocess_text(text):
    text = text.lower()
    tokens = word_tokenize(text)
    tokens = [token for token in tokens if token.isalpha()]
    return ' '.join(tokens)


# Function to preprocess a list of texts
def preprocess_texts(texts):
    return [preprocess_text(text) for text in texts]

# Create a FunctionTransformer for text preprocessing
text_preprocessor = FunctionTransformer(preprocess_texts, validate=False)

# To load and recreate the model in another place:
loaded_tfidf_vocabulary = pd.read_parquet('app/data/tfidf_vocabulary.parquet')
loaded_nb_params = pd.read_parquet('app/data/nb_params.parquet')
loaded_tfidf_idf = np.load('app/data/tfidf_idf.npy')

# Recreate TF-IDF Vectorizer
new_tfidf = TfidfVectorizer(vocabulary=dict(zip(loaded_tfidf_vocabulary.index, loaded_tfidf_vocabulary['index'])))
new_tfidf.idf_ = loaded_tfidf_idf
new_tfidf._tfidf._idf_diag = sp.spdiags(new_tfidf.idf_, diags=0, m=len(new_tfidf.idf_), n=len(new_tfidf.idf_))

# Recreate Naive Bayes Classifier
new_nb = MultinomialNB()
new_nb.feature_count_ = np.array(loaded_nb_params['feature_count'].tolist())
new_nb.class_count_ = np.array(loaded_nb_params['class_count'].tolist())
new_nb.class_log_prior_ = np.array(loaded_nb_params['class_log_prior'].tolist())
new_nb.feature_log_prob_ = np.array(loaded_nb_params['feature_log_prob'].tolist())
new_nb.classes_ = np.array(loaded_nb_params['classes'].tolist())

# Recreate Pipeline
invoice_payment_status_classifier_v1 = Pipeline([
    ('preprocessor', text_preprocessor),
    ('tfidf', new_tfidf),
    ('clf', new_nb),
])


def predict_payment_status(invoice_raw_text: str, model=None):
    if model is None:
        model = invoice_payment_status_classifier_v1
    preprocessed_text = preprocess_text(invoice_raw_text)
    return str(model.predict([preprocessed_text])[0])


def ocr_from_image_url(image_url: str) -> str:
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    # Set language to Polish and use PSM 6 for dense text"
    custom_config = r'--oem 3 --psm 6 -l pol'
    return pytesseract.image_to_string(img, config=custom_config)


app = FastAPI()


@app.get('/')
def health_check():
    return {'health_check': 'OK'}


@app.get('/info')
def info():
    return {'name': 'ml_deploy_test',
            'working_directory': os.getcwd(),
            'working_directory_2': os.path.dirname(os.path.realpath(__file__))}


@app.get('/predict')
def predict(invoice_raw_text: str):
    return {'prediction': predict_payment_status(invoice_raw_text)}


@app.get('/ocr_image')
def predict_from_image(image_url: str):
    return {'ocr_raw_text': ocr_from_image_url(image_url)}
