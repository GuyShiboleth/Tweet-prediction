import streamlit as st
import random
import numpy as np

# Create the info sidebar
def create_info(html_link):
    container = st.container()
    with container:
        info_expander = st.sidebar.expander("Info about this website")
        info_expander.write("This is a website I created as a part of my final's project in my machine learning class. in this website, you can enter a \"politician tweet\" wether real or fake. using 2 NLP models I created with custom transformers, the website will try and guess the age of the person who wrote the tweet and their political party (republican or democrat).")
        info_expander.write(" After guessing the age and party of the person who wrote the tweet it will showcase the politician who's age and party are the most similar to the predicted person.")
        info_expander.write("The tweets here only have 140 characters because that's the max amount I could fetch without leaving my computer running for days. The tweets over the 140 character limit have an elipses at their end.")
        info_expander.write("The models were trained using the Keras library which is a part of TensorFlow in Python. They were trained on a custom database of senator tweets which you can see here:")
        info_expander.write(html_link,unsafe_allow_html=True)

# Create the base text
def create_base():
    st.markdown(
        """
        <style>
        .container {
            display: inline-flex;
            flex-direction: row;
            align-items: center;
            border-radius: 5px;
            font-size:250%;
            font-family:sans-serif;
            font-weight:bold;
        }
        .text {
            margin-right: 5px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="container"><span class="text">What politician are you?</span></div>', unsafe_allow_html=True)

    st.header("Let's find out🔍")

    option = st.radio("type of text",['Your own tweet','Existing senate tweet','Pick a random senators tweet'], index=0, label_visibility="hidden")
    return option


# Display the correct instructions and objects according to the option selected
def display_task(option,df):
    st.markdown(
            """
            <style>
            .explain {
                display: inline-flex;
                flex-direction: row;
                align-items: center;
                border-radius: 5px;
                font-size:120%;
                font-family:sans-serif;
                font-weight:bold;
            }
            .text {
                margin-right: 5px;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
    
    if option=="Your own tweet":
        st.markdown('<div class="explain"><span class="text">Write a tweet either for a politician or as a politician. We will guess your/the politician you are writing for\'s age, party, state and the most closely resembeling senate member.</span></div>',unsafe_allow_html=True)

        tweet = st.text_input("write your political tweet here", value="", max_chars=280, type="default",placeholder="Enter your political tweet here",label_visibility='hidden')
        return [tweet,-1]
    

    if option=="Existing senate tweet":
        st.markdown('<div class="explain"><span class="text">Enter a value between 0 and 263994. The website will chose the corresponding model from the dataset. Then the model will guess what politician wrote it and we\'ll see wether it is right or wrong. if the model is wrong it will show you information about the 2 politicians to see wether there are any similarities.</span></div>',unsafe_allow_html=True)
        st.markdown('the relevant indexes are the ones on the 1st column from the left')
        
        tweet_num=st.number_input("tweetnum", min_value=0, max_value=249974, value=0, step=1, label_visibility="hidden")
        st.dataframe(df)
        
        return [df['tweet_text'][tweet_num],tweet_num]
    

    if option=="Pick a random senators tweet":
        random_num = random.randint(0,249974)
        tweet=df['tweet_text'][random_num]
        st.markdown(f"the number selected is {random_num} and the corresponding tweet is:")
        st.markdown(f"{tweet}")
        return [tweet,random_num]

def show_results(predictions,index,df,option):
    if predictions==0:
        return

    if predictions==-1:
        st.markdown("The model needs to know at least three words it knows to infer attributes, please try a different tweet.")
    else:
        [senator,state,party,age]=predictions
        if option=="Your own tweet":
            st.subheader("The most closely resembling attributes are:")
            st.caption("Please note: there isn't a correlation between the senator predicted and the remaining attributes, they are calculated predicted seperately")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Age", value=int(np.round(age)))
            with col2:
                st.metric(label="Party", value=party)
            col3, col4 = st.columns(2)
            with col3:
                st.metric(label="State", value=state)
            with col4:
                st.metric(label="Senator", value=senator)
            

        else:
            st.subheader("The actual attributes are:")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric('Age', df['age'][index], label_visibility="visible")
            with col2:
                st.metric('Party', df['party'][index], label_visibility="visible")
            col3, col4 = st.columns(2)
            with col3:
                st.metric('State', df['state name'][index], label_visibility="visible")
            with col4:
                st.metric('Senator', df['senator name'][index], label_visibility="visible")
            
            
            st.subheader("The predicted attributes are:")
            col5, col6 = st.columns(2)
            with col5:
                st.metric(label="Age",value=int(np.round(age)))
            with col6:
                st.metric(label="Party",value=party)
            col7, col8 = st.columns(2)
            with col7:
                st.metric(label="State", value=state)
            with col8:
                st.metric(label="Senator", value=senator)

def random_button():
    st.button("another random",type="primary")
