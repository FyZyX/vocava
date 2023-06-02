import io
import json
import time

import openai
import streamlit as st
from streamlit_chat import message as chat_message

from vocava import storage, entity
from vocava.llm import LanguageModel
from vocava.llm.prompt import load_prompt
from vocava.service import Service
from vocava.st_custom_components import st_audiorec

ANTHROPIC_API_KEY = st.secrets["anthropic_api_key"]
COHERE_API_KEY = st.secrets["cohere_api_key"]
openai.api_key = st.secrets["openai_api_key"]


def get_audio_transcript():
    data = st_audiorec()
    if not data:
        return None

    file = io.BytesIO(data)
    file.name = "tmp.wav"
    with st.spinner():
        response = openai.Audio.transcribe("whisper-1", file)
    return response["text"]


def main():
    st.header("Chatterbox")

    db = storage.VectorStore(COHERE_API_KEY)
    db.connect()

    debug_mode = st.sidebar.checkbox("DEBUG Mode", value=True)
    model = "Claude" if not debug_mode else "mock"
    tutor = entity.get_tutor(model, key=ANTHROPIC_API_KEY)

    native_language = st.sidebar.selectbox("Native Language", options=entity.LANGUAGES)
    target_language = st.sidebar.selectbox(
        "Choose Language", options=entity.LANGUAGES, index=4)
    fluency = st.sidebar.slider("Fluency", min_value=1, max_value=10, step=1)
    user = entity.User(
        native_language=native_language,
        target_language=target_language,
        fluency=fluency,
    )

    input_method = st.sidebar.radio("Input method", ("Text Input", "Voice Input"))
    view_native = st.sidebar.checkbox("View in native language")

    if input_method == "Text Input":
        user_input = st.text_input("Enter a Message")
    elif input_method == "Voice Input":
        user_input = get_audio_transcript()
    else:
        return

    if "chatterbox.history" not in st.session_state:
        st.session_state["chatterbox.history"] = []

    if st.button("Send"):
        chatterbox = Service(
            name="chatterbox",
            user=user,
            tutor=tutor,
            max_tokens=150,
            native_mode=view_native,
        )
        history = st.session_state["chatterbox.history"]
        chat_history = "\n".join([
            f'USER: {interaction["user"][user.target_language_name()]}\n'
            f'TUTOR: {interaction["tutor"][user.target_language_name()]}'
            for interaction in history
        ])
        with st.spinner():
            data = chatterbox.run(history=chat_history, message=user_input)

        interaction = data["interaction"]
        if interaction:
            db.save_interaction(interaction)
        st.session_state["chatterbox.history"].append(interaction)
        st.session_state["chatterbox.language"] = chatterbox.current_language()

    history = st.session_state["chatterbox.history"][::-1]
    if not history:
        return
    last_interaction = history[0]

    language = st.session_state["chatterbox.language"]
    user_message = last_interaction["user"][language]
    tutor_message = last_interaction["tutor"][language]
    corrected = last_interaction["user"].get(
        f"{user.target_language_name()}_corrected"
    )
    explanation = last_interaction["user"].get(
        f"{user.native_language_name()}_explanation"
    )
    if corrected:
        st.warning(corrected)
        st.info(explanation)

    for i, interaction in enumerate(history):
        chat_message(tutor_message, key=f"{i}")
        chat_message(user_message, is_user=True, key=f"{i}_user")


if __name__ == "__main__":
    main()
