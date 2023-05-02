import streamlit as st
import pandas as pd
from view import *
from controller import *
from custom_layers import *
import keras


#שימוש בשם אחר לעמוד ומתן אייקון לעמוד
st.set_page_config(
    page_title="Political tweet predicter",
    page_icon='🏛️',
    layout="wide",
    initial_sidebar_state="expanded",
)
# upload dataframe and models
df=upload_ds()
models = upload_models()
tokenizer = upload_tokenizer()
label_encoders = upload_label_encoders()


# Create a link to use in html for the purpose of adding the dataset
html_link=create_html_link()

#Create info page
create_info(html_link)

# Create the base of the website
option=create_base()

# Handle the radio input
[tweet,index]=display_task(option,df)

predictions = use_model(tweet,models,tokenizer,label_encoders)

show_results(predictions,index,df,option)

if option == 'Pick a random senators tweet':
    random_button()