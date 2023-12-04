import streamlit as st
from src.openai_utils import get_quiz_data
from src.quiz_utils import get_randomized_options
import os
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_TOKEN")




st.title("Hello There! 👋")
st.subheader("Welcome to who will win the dollar quiz 🎉")
st.text("")
st.text("Please answer the questions below to get started")
st.text("")

with st.expander("How to use ?"):
    st.text("1- Choose the topic you would like to get the quiz in")
    st.text("2- Choose the number of questions you would like to answer")
    st.text("3- Answer the right answer for each question and get points!")

with st.form("user_input"):
    TOPIC_TEXT = st.text_input("Enter the Topic:", placeholder="football, streamlit, etc...")
    NUMBER_OF_QUESTIONS = st.text_input("Enter the number of questions:", placeholder="1")
    submitted = st.form_submit_button("Let's start!")

if submitted or ('quiz_data_list' in st.session_state):
    if not TOPIC_TEXT:
        st.info("Please provide a Topic")
        st.stop()
    elif not NUMBER_OF_QUESTIONS:
        st.info("Please provide the number of questions")
        st.stop()

    with st.spinner("Your quiz is under the making...🫵"):
        if submitted:
            st.session_state.randomized_options = [] 
            print("Debug: Cleared randomized options")
            quiz_data = get_quiz_data(TOPIC_TEXT, int(NUMBER_OF_QUESTIONS), openai_api_key)
            st.session_state.quiz_data_list = quiz_data

            st.session_state.user_answers = []

            if 'correct_answers' not in st.session_state:
                st.session_state.correct_answers = []
            if 'randomized_options' not in st.session_state:
                st.session_state.randomized_options = []

            for opt in st.session_state.quiz_data_list:
                options, correct_answer = get_randomized_options(opt[1:])
                st.session_state.randomized_options.append(options)
                st.session_state.correct_answers.append(correct_answer)

        with st.form(key='quiz_form'):
            st.subheader("Test Your Knowledge!", anchor=False)
            for i, q in enumerate(st.session_state.quiz_data_list):
                options = st.session_state.randomized_options[i]
                default_index = st.session_state.user_answers[i] if st.session_state.user_answers and i < len(st.session_state.user_answers) and st.session_state.user_answers[i] is not None else 0
                response = st.radio(q[0], options, index=default_index)
                user_choice_index = options.index(response)
                st.session_state.user_answers.append(user_choice_index)

            results_submitted = st.form_submit_button(label='Unveil My Score!')

            if results_submitted:
                score = 0
                num_questions = len(st.session_state.quiz_data_list)
                for i in range(num_questions):
                    if i < len(st.session_state.randomized_options):
                        ua = st.session_state.user_answers[i] if i < len(st.session_state.user_answers) else None
                        ca = st.session_state.correct_answers[i] if i < len(st.session_state.correct_answers) else None
                        if ua is not None and 0 <= ua < len(st.session_state.randomized_options[i]):
                            if st.session_state.randomized_options[i][ua] == st.session_state.quiz_data_list[i][1]:
                                score += 1
                        else:
                            pass
                    else:
                        pass
                st.success(f"Your score: **{score}/{len(st.session_state.quiz_data_list)}**")

                if score == len(st.session_state.quiz_data_list):
                    st.balloons()
                else:
                    incorrect_count = len(st.session_state.quiz_data_list) - score
                    if incorrect_count == 1:
                        st.warning(f"Almost perfect! You got 1 question wrong. Let's review it:")
                    else:
                        st.warning(f"Almost there! You got **{incorrect_count}** questions wrong. Let's review them:")

                for i, (ua, ca, q, ro) in enumerate(
                        zip(st.session_state.user_answers, st.session_state.correct_answers,
                            st.session_state.quiz_data_list, st.session_state.randomized_options)):
                    with st.expander(f"Question **{i + 1}**", expanded=False):
                        if ro[ua] != ca:
                            st.info(f"Question: **{q[0]}**")
                            if ro[ua] != ca:
                                st.error(f"Your answer: **{ro[ua]}**")
                            else:
                                st.success(f"Your answer: **{ro[ua]}**")    
                            st.success(f"Correct answer is option: **{ca}**")
