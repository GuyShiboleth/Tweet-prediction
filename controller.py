import streamlit as st
import pandas as pd
import keras
import numpy as np
import sklearn.preprocessing as skpre
import pickle
from keras.utils import pad_sequences


#upload the tweets dataset
@st.cache_data
def upload_ds():
    pd.set_option('display.max_colwidth', None)
    dataset=pd.read_excel("base_ds.xlsx")
    return dataset

@st.cache_data
def upload_label_encoders():
    senator_encoder = skpre.LabelEncoder()
    senator_encoder.classes_ = np.load('models/Senator/senatorclasses.npy',allow_pickle=True)
    
    state_encoder = skpre.LabelEncoder()
    state_encoder.classes_ = np.load('models/State/stateclasses.npy',allow_pickle=True)
    
    party_encoder = skpre.LabelEncoder()
    party_encoder.classes_ = np.load('models/Party/partyclasses.npy',allow_pickle=True)

    return [senator_encoder,state_encoder,party_encoder]

@st.cache_data
def upload_tokenizer():
    with open(r'models\tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
        return tokenizer

# upload the models
@st.cache_resource
def upload_models():
    senator = keras.models.load_model("models/Senator")
    state = keras.models.load_model('models/State')
    party = keras.models.load_model("models/Party")
    age = keras.models.load_model("models/Age")

    return [senator,state,party,age]


# Add link to dataset
def create_html_link(link="https:/drive.google.com/file/d/1GolL127hFgWpDx1V99mBnZwxdKXHEyUC/view?usp=share_link",text="link to dataset"):
    html_link = f'<a href="{link}" target="_blank">{text}</a>'
    return html_link


# Handle the chosen radio option
def use_model(tweet,models,tokenizer,label_encoders):
    
    max_len=140
    senator_prediction=''
    state_prediction=''
    party_prediction=''
    
    senator_label_encoder=  label_encoders[0]
    senator_model = models[0]

    state_label_encoder=  label_encoders[1]
    state_model = models[1]

    party_model = models[2]

    age_model = models[3]
    
        
    corpus = [tweet]
    tokenized_corpus = tokenizer.texts_to_sequences(corpus)
    padded_corpus = pad_sequences(tokenized_corpus, maxlen=max_len)
        
    senator_prediction_array = senator_model.predict(padded_corpus)
    senator_prediction_index = np.argmax(senator_prediction_array, axis=-1)
    senator_prediction = senator_label_encoder.inverse_transform([senator_prediction_index])[0]

    state_prediction_array = state_model.predict(padded_corpus)
    state_prediction_index = np.argmax(state_prediction_array, axis=-1)
    state_prediction = state_label_encoder.inverse_transform([state_prediction_index])[0]

    party_prediction_array = party_model.predict(padded_corpus)
    if party_prediction_array[0][0]>=0.5:
        party_prediction = "Republican"
    else:
        party_prediction= "Democratic"

    age_prediction = age_model.predict(padded_corpus)


    has_three_known = len([x for x in tokenized_corpus[0] if x != 1]) >= 3
    if has_three_known:
        return [senator_prediction,state_prediction,party_prediction,age_prediction]
    elif tweet=='':
        return 0
    else: 
        return -1
