import openai
import os
import streamlit as st
from streamlit_chat import message

# define a history if there is none
if "history" not in st.session_state:
    st.session_state.history = [{"role": "system", "content": "You are a helpful assistant"}]


# changing the openai key
def change_key():
    st.session_state.openai_key = st.session_state.openai_key

# execute openai command and add the result into history
def execute_openai():
    if st.session_state.input:
        st.session_state.history.append({"role": "user", "content": st.session_state.input})
    else:
        st.error("Please enter a message")
        return
    
    # check for openai key
    if not st.session_state.openai_key:
        st.error("Please enter an OpenAI key")
        return

    # embed the key & run the model
    openai.api_key = st.session_state.openai_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.history
    )

    # add the response to the history
    st.session_state.output = response.choices[0].message.content
    st.session_state.history.append({"role": "assistant", "content": f'''{response.choices[0].message.content}'''})
    print_history()



def print_history():
    # print the history if its not system & clear the input
    for i in st.session_state.history:
        if i["role"] == "system":
            continue
        elif i["role"] == "assistant":
            message(f'''{i["content"]}''', is_user=False)
        else:
            message(i["content"], is_user=True)
    st.session_state.input = ""


st.text_input("Type something", key="input", on_change=execute_openai, placeholder="Hello, how are you?")
st.text_input("OpenAI Key", key="openai_key", on_change=change_key, placeholder="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
