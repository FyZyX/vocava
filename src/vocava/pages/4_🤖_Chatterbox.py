import io

import openai
import streamlit as st
from streamlit_chat import message as chat_message

from vocava import translate, storage
from vocava.llm import anthropic, mock
from vocava.st_custom_components import st_audiorec

DEBUG = True
ANTHROPIC_API_KEY = st.secrets["anthropic_api_key"]
COHERE_API_KEY = st.secrets["cohere_api_key"]
openai.api_key = st.secrets["openai_api_key"]


class User:
    @staticmethod
    def _get_text(default=""):
        return st.text_input("Enter a Message", default)

    @staticmethod
    def _get_audio_transcript():
        data = st_audiorec()
        if not data:
            return None

        file = io.BytesIO(data)
        file.name = "tmp.wav"
        with st.spinner():
            response = openai.Audio.transcribe("whisper-1", file)
        return response["text"]

    def get_input(self):
        input_method = st.radio("Input method", ("Text Input", "Voice Input"))
        if input_method == "Text Input":
            return self._get_text()
        elif input_method == "Voice Input":
            return self._get_audio_transcript()


def send_message(user_input, native_lang, target_lang):
    if DEBUG:
        model = mock.MockLanguageModel()
        bot = mock.MockLanguageModel()
    else:
        model = anthropic.Claude(ANTHROPIC_API_KEY)
        bot = anthropic.ClaudeChatBot(ANTHROPIC_API_KEY)

    translator = translate.Translator(model)
    chatterbox = translate.Chatterbox(
        bot, translator, native_lang, target_lang
    )
    interaction = chatterbox.start_interaction(user_input)

    st.session_state['history'].append(interaction.json())
    return interaction


def get_user_input():
    db = storage.VectorStore(COHERE_API_KEY)
    db.connect()

    col1, col2 = st.columns(2)
    native_lang = col1.text_input("Your native language: ", "en")
    target_lang = col2.text_input("Your target language: ", "fr")

    user = User()
    user_input = user.get_input()
    if user_input:
        interaction = send_message(user_input, native_lang, target_lang)
        db.save(
            ids=interaction.ids(),
            documents=interaction.documents(),
            metadata=interaction.metadata(),
        )

    view_target = st.checkbox('View in target language')
    language = target_lang if view_target else native_lang
    return language


def render_chat_history(language):
    for i in range(len(st.session_state['history']) - 1, -1, -1):
        message = st.session_state["history"][i]
        chat_message(message['bot'][language], key=f"{i}")
        chat_message(message['user'][language], is_user=True, key=f'{i}_user')


def main():
    st.header("Vocava")

    if 'history' not in st.session_state:
        st.session_state['history'] = []

    view_language = get_user_input()
    if st.session_state['history']:
        render_chat_history(view_language)


if __name__ == '__main__':
    main()
