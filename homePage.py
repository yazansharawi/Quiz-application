import streamlit as st
from src.openai_utils import get_quiz_data
from src.quiz_utils import get_randomized_options
import os
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_TOKEN")

st.title("Hello There! 👋")
st.subheader("Welcome to the 'Who Will Win the Dollar' quiz 🎉")
st.text("Please answer the questions below to get started")

with st.expander("How to use?"):
    st.text("1- Choose the topic you would like to get the quiz in")
    st.text("2- Choose the number of questions you would like to answer")
    st.text("3- Answer the right answer for each question and get points!")

with st.form("user_input"):
    TOPIC_TEXT = st.text_input("Enter the Topic:", placeholder="football, streamlit, etc...")
    NUMBER_OF_QUESTIONS = st.text_input("Enter the number of questions:", placeholder="1")
    submitted = st.form_submit_button("Let's start!",type="primary")

if submitted or ('quiz_data_list' in st.session_state):
    if not TOPIC_TEXT:
        st.info("Please provide a Topic")
        st.stop()
    elif not NUMBER_OF_QUESTIONS:
        st.info("Please provide the number of questions")
        st.stop()

    with st.spinner("Your quiz is under the making...🫵"):
        if submitted:
            quiz_data = get_quiz_data(TOPIC_TEXT, int(NUMBER_OF_QUESTIONS), openai_api_key)
            st.session_state.quiz_data_list = quiz_data
            st.session_state.user_answers = [None] * len(st.session_state.quiz_data_list)
            st.session_state.correct_answers = []
            st.session_state.randomized_options = []

            for opt in st.session_state.quiz_data_list:
                options, correct_answer = get_randomized_options(opt[1:])
                st.session_state.randomized_options.append(options)
                st.session_state.correct_answers.append(correct_answer)

        with st.form(key='quiz_form'):
            st.subheader("Test Your Knowledge!", anchor=False)
            for i, q in enumerate(st.session_state.quiz_data_list):
                options = st.session_state.randomized_options[i]
                default_index = 0
                response = st.radio(q[0], options, index=default_index, key=f"question_{i}")
                user_choice_index = options.index(response)
                st.session_state.user_answers[i] = user_choice_index

            results_submitted = st.form_submit_button(label='Unveil My Score!')

            if results_submitted:
                score = 0
                for i in range(len(st.session_state.quiz_data_list)):
                    user_answer_text = st.session_state.randomized_options[i][st.session_state.user_answers[i]]
                    correct_answer_text = st.session_state.quiz_data_list[i][1]
                    if user_answer_text == correct_answer_text:
                        score += 1

                st.success(f"Your score: **{score}/{len(st.session_state.quiz_data_list)}**")

                if score == len(st.session_state.quiz_data_list):
                    st.balloons()
                else:
                    incorrect_count = len(st.session_state.quiz_data_list) - score
                    st.warning(f"Review: You got **{incorrect_count}** questions wrong.")

                for i in range(len(st.session_state.quiz_data_list)):
                    if st.session_state.randomized_options[i][st.session_state.user_answers[i]] != st.session_state.quiz_data_list[i][1]:
                        with st.expander(f"Question {i + 1} Review", expanded=False):
                            st.info(f"Question: **{st.session_state.quiz_data_list[i][0]}**")
                            st.error(f"Your answer: **{st.session_state.randomized_options[i][st.session_state.user_answers[i]]}**")
                            st.success(f"Correct answer: **{st.session_state.quiz_data_list[i][1]}**")
