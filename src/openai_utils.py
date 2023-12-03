from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.chains import LLMChain
import openai
import streamlit as st

def get_quiz_data(text, num_questions, openai_api_key):
    template = f"""
    You are a helpful assistant programmed to generate questions based on any text provided. For every chunk of text you receive, you're tasked with designing {num_questions} distinct questions. Each of these questions will be accompanied by 4 possible answers: one correct answer and three incorrect ones.

    For clarity and ease of processing, structure your response in a way that emulates a Python list of lists.

    Your output should be shaped as follows:

    Your output should mirror this structure:

    [
        ["Generated Question 1", "Correct Answer 1", "Incorrect Answer 1.1", "Incorrect Answer 1.2", "Incorrect Answer 1.3"],
        ["Generated Question 2", "Correct Answer 2", "Incorrect Answer 2.1", "Incorrect Answer 2.2", "Incorrect Answer 2.3"],
        ...
    ]

    It is crucial that you adhere to this format as it's optimized for further Python processing.
    """

    try:
        system_message_prompt = SystemMessagePromptTemplate.from_template(template)
        human_message_prompt = HumanMessagePromptTemplate.from_template("{text}")
        chat_prompt = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt]
        )
        chain = LLMChain(
            llm=ChatOpenAI(openai_api_key=openai_api_key),
            prompt=chat_prompt,
        )
        generated_text = chain.run(text)

        if not generated_text.strip():
            st.warning("Warning: The generated text is empty.")
        else:
            print("all good")

        # Split the generated_text into questions and options
        lines = generated_text.strip().split('\n')
        questions = [lines[i:i+5] for i in range(0, len(lines), 5)]

        return questions

    except openai.error.OpenAIError as e:
        st.error(f"An error occurred: {str(e)}")
        st.stop()
    except Exception as e:
        if "AuthenticationError" in str(e):
            st.error("Incorrect API key provided. Please check and update your API key.")
            st.stop()
        else:
            st.error(f"An unexpected error occurred: {str(e)}")
            st.stop()
