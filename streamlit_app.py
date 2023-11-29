import streamlit as st
import numpy as np
from langchain.llms import OpenAI
import requests

st.set_page_config(page_title="🦜🔗 Quickstart App")
st.title('🦜🔗 Quickstart App')

openai_api_key = st.sidebar.text_input('OpenAI API Key')

def generate_response(input_text):
  
  system_prompt = "Please provide concise, clear, and helpful advice on: "
  combined_input = system_prompt + input_text
  llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
  st.info(llm(combined_input))
  text_to_speech(combined_input)


#########################
def text_to_speech(input_text):
    url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"
    headers = {
      "Accept": "audio/mpeg",
      "Content-Type": "application/json",
      "xi-api-key": "4d88e61bfeea05215c590639d56bdff2"
    }
    data = {
      "text": input_text,
      "model_id": "eleven_monolingual_v1",
      "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.5
      }
    }
    response = requests.post(url, json=data, headers=headers)
    audio_file_path = 'output.mp3'
    with open(audio_file_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return audio_file_path





###########################

with st.form('my_form'):
  text = st.text_area('Enter text:', '?io')
  submitted = st.form_submit_button('Submit')
  if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
  if submitted and openai_api_key.startswith('sk-'):
    generate_response(text)


####


audio_file = open('output.mp3', 'rb')
audio_bytes = audio_file.read()

st.audio(audio_bytes, format='a')

# sample_rate = 44100  # 44100 samples per second
# seconds = 2  # Note duration of 2 seconds
# frequency_la = 440  # Our played note will be 440 Hz
# # Generate array with seconds*sample_rate steps, ranging between 0 and seconds
# t = np.linspace(0, seconds, seconds * sample_rate, False)
# # Generate a 440 Hz sine wave
# note_la = np.sin(frequency_la * t * 2 * np.pi)

#st.audio(note_la, sample_rate=sample_rate)
