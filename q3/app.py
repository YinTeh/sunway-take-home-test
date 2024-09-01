import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from crewai import Crew, Process
from tasks import research_task, write_task
from agents import news_researcher, news_writer

load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def clear_chat_history():
    st.session_state.messages = [
        {"role": "assistant", "content": "upload some pdfs and ask me a question"}]


def main():
    crew = Crew(
        agents=[news_researcher, news_writer],
        tasks=[research_task, write_task],
        process=Process.sequential,
    )
    st.set_page_config(
        page_title="Gemini RAG research bot",
        page_icon="🤖"
    )

    # Main content area for displaying chat messages
    st.title("Chat with research agent Gemini🤖")
    st.write("Welcome to the chat!")
    st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

    # Chat input
    # Placeholder for chat messages

    if "messages" not in st.session_state.keys():
        st.session_state.messages = [
            {"role": "assistant", "content": "Ask me a question"}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    # Display chat messages and bot response
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # response = user_input(prompt)
                response = crew.kickoff(inputs={'topic': prompt})
                placeholder = st.empty()
                # full_response = ''
                # for item in response['output_text']:
                #     full_response += item
                #     placeholder.markdown(full_response)
                placeholder.markdown(response)
        if response is not None:
            message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message)


if __name__ == "__main__":
    main()
