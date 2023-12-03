import streamlit as st
from src.openai_utils import get_quiz_data
from src.quiz_utils import get_randomized_options



st.title("Hello There! 👋")
st.subheader("Welcome to who will win the dollar quiz 🎉")
st.text("")
st.text("Please answer the questions below to get started")
st.text("")

with st.expander("How to use ?"):
    st.text("1- Chosse your the topic you would like to get the quiz in")
    st.text("2- Chosse the number of questions you would like to answer")
    st.text("3- Answer the right answer for each question and get points!")

with st.form("user_input"):
    TOPIC_TEXT = st.text_input("Enter the Topic:", placeholder="football,streamlit,etc...")
    NUMBER_OF_QUESTIONS = st.text_input("Enter the number of questions:", placeholder="1")
    submitted = st.form_submit_button("Let's start!")

if submitted or ('quiz_data_list' in st.session_state):
    if not  TOPIC_TEXT:
        st.info("Please provide a Topic")
        st.stop()
    elif not NUMBER_OF_QUESTIONS:
        st.info("Please provide the number of questions")
        st.stop()
        
    with st.spinner("Your quiz is under the making...🤓"):
        if submitted:
            quiz_data = get_quiz_data(TOPIC_TEXT,int(NUMBER_OF_QUESTIONS) ,"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")
            st.session_state.quiz_data_list = quiz_data
            print("st.session_state.quiz_data_list",st.session_state.quiz_data_list)
