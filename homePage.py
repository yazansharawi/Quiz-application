import streamlit as st
from src.openai_utils import get_quiz_data
from src.quiz_utils import string_to_list, get_randomized_options



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
            st.session_state.quiz_data_list = string_to_list(quiz_data)
            
            if 'user_answers' not in st.session_state:
                st.session_state.user_answers = [None for _ in st.session_state.quiz_data_list]
            if 'correct_answers' not in st.session_state:
                st.session_state.correct_answers = []
            if 'randomized_options' not in st.session_state:
                st.session_state.randomized_options = [] 
            for q in st.session_state.quiz_data_list:
                options, correct_answer = get_randomized_options(q[1:])
                st.session_state.randomized_options.append(options)
                st.session_state.correct_answers.append(correct_answer)
                print("st.session_state.correct_answers",st.session_state.correct_answers)

        with st.form(key='quiz_form'):
            st.subheader("Test Your Knowledge!", anchor=False)
            for i, q in enumerate(st.session_state.quiz_data_list):
                options = st.session_state.randomized_options[i]
                default_index = st.session_state.user_answers[i] if st.session_state.user_answers[i] is not None else 0
                response = st.radio(q[0], options, index=default_index)
                user_choice_index = options.index(response)
                st.session_state.user_answers[i] = user_choice_index 


            results_submitted = st.form_submit_button(label='Unveil My Score!')

            if results_submitted:
                score = sum([ua == st.session_state.randomized_options[i].index(ca) for i, (ua, ca) in enumerate(zip(st.session_state.user_answers, st.session_state.correct_answers))])
                st.success(f"Your score: {score}/{len(st.session_state.quiz_data_list)}")

                if score == len(st.session_state.quiz_data_list): 
                    st.balloons()
                else:
                    incorrect_count = len(st.session_state.quiz_data_list) - score
                    if incorrect_count == 1:
                        st.warning(f"Almost perfect! You got 1 question wrong. Let's review it:")
                    else:
                        st.warning(f"Almost there! You got {incorrect_count} questions wrong. Let's review them:")

                for i, (ua, ca, q, ro) in enumerate(zip(st.session_state.user_answers, st.session_state.correct_answers, st.session_state.quiz_data_list, st.session_state.randomized_options)):
                    with st.expander(f"Question {i + 1}", expanded=False):
                        if ro[ua] != ca:
                            st.info(f"Question: {q[0]}")
                            st.error(f"Your answer: {ro[ua]}")
                            st.success(f"Correct answer: {ca}")