import io

import cohere
import openai
import streamlit as st
from streamlit_chat import message as chat_message

from vocava import translate, storage
from vocava.st_custom_components import st_audiorec
from vocava.llm import anthropic, mock

DEBUG = True
ANTHROPIC_API_KEY = st.secrets["anthropic_api_key"]
COHERE_API_KEY = st.secrets["cohere_api_key"]
openai.api_key = st.secrets["openai_api_key"]


class User:
    @staticmethod
    def get_text(default=""):
        return st.text_input("Enter a Message", default)

    @staticmethod
    def get_audio_transcript():
        data = st_audiorec()
        if not data:
            return None

        file = io.BytesIO(data)
        file.name = "tmp.wav"
        with st.spinner():
            response = openai.Audio.transcribe("whisper-1", file)
        return response["text"]


def embed(docs: list[str]):
    cohere_client = cohere.Client(api_key=COHERE_API_KEY)
    return cohere_client.embed(texts=docs, model='embed-english')


def send_message(user_input, native_lang, target_lang, db: storage.VectorStore):
    model = anthropic.Claude(ANTHROPIC_API_KEY)
    model = mock.MockLanguageModel()
    translator = translate.Translator(model)
    bot = anthropic.ClaudeChatBot(ANTHROPIC_API_KEY)
    bot = mock.MockLanguageModel()
    translation_bot = translate.TranslationLanguageModel(
        bot, translator, native_lang, target_lang, db
    )

    completion = translation_bot.generate(user_input)

    st.session_state['history'].append(translation_bot.last_translation())
    return completion


def get_user_input():
    db = storage.VectorStore(COHERE_API_KEY)
    db.connect()

    col1, col2 = st.columns(2)
    native_lang = col1.text_input("Your native language: ", "en")
    target_lang = col2.text_input("Your target language: ", "fr")

    user = User()
    input_method = st.radio("Input method", ("Text Input", "Voice Input"))
    if input_method == "Text Input":
        user_input = user.get_text()
        if user_input:
            send_message(user_input, native_lang, target_lang, db)
    elif input_method == "Voice Input":
        user_input = user.get_audio_transcript()
        if user_input:
            send_message(user_input, native_lang, target_lang, db)

    view_target = st.checkbox('View in target language')
    language = target_lang if view_target else native_lang
    return language


def render_chat_history(language):
    for i in range(len(st.session_state['history']) - 1, -1, -1):
        message = st.session_state["history"][i]
        chat_message(message['bot'][language], key=f"{i}")
        chat_message(message['user'][language], is_user=True, key=f'{i}_user')


def main():
    st.set_page_config(
        page_title="Vocava - Demo",
        page_icon=":robot:"
    )

    st.header("Vocava")

    if 'history' not in st.session_state:
        st.session_state['history'] = []

    view_language = get_user_input()
    if st.session_state['history']:
        render_chat_history(view_language)


if __name__ == '__main__':
    main()
