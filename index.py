import openai
import os
import streamlit as st
from streamlit_chat import message
import pyaudio
import wave
import whisper
import numpy

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

def whisper_api(wf):
    model = whisper.load_model("base")
    result = model.transcribe(wf)
    

def record_audio():
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 2
    fs = 44100
    seconds = 3
    filename = "output.wav"

    p = pyaudio.PyAudio()

    print('Recording')

    stream = p.open(
        format=sample_format,
        channels=channels,
        rate=fs,
        frames_per_buffer=chunk,
        input=True)
    
    frames = []

    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(numpy.fromstring(data, dtype=numpy.int16))

    numpydata = numpy.hstack(frames)
    
    stream.stop_stream()
    stream.close()
    p.terminate()

    print('Finished recording')

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    whisper_api(filename)
    wf.close()
    


st.text_input("Type something", key="input", on_change=execute_openai, placeholder="Hello, how are you?")
st.button("Record", key="record", on_click=record_audio)
st.text_input("OpenAI Key", key="openai_key", on_change=change_key, placeholder="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
