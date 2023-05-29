import io
import time

import openai
import streamlit as st
from streamlit_chat import message as chat_message

from vocava import translate, storage
from vocava.llm import anthropic, mock, LanguageModel
from vocava.st_custom_components import st_audiorec
from vocava.translate import Translator

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


class Interaction:
    def __init__(self, documents, start_language, end_language):
        self._documents = documents
        self._start_language = start_language
        self._end_language = end_language

    def ids(self):
        message_id = int(time.time())
        return [
            f"{message_id}-user-{self._start_language}",
            f"{message_id}-user-{self._end_language}",
            f"{message_id}-bot-{self._end_language}",
            f"{message_id}-bot-{self._start_language}",
        ]

    def documents(self):
        return self._documents

    def metadata(self):
        return [
            {"language": self._start_language},
            {"language": self._end_language},
            {"language": self._end_language},
            {"language": self._start_language},
        ]

    def json(self):
        return {
            "user": {
                self._start_language: self._documents[0],
                self._end_language: self._documents[1],
            },
            "bot": {
                self._end_language: self._documents[2],
                self._start_language: self._documents[3],
            },
        }


class Chatterbox:
    def __init__(self, user: User, user_language: str,
                 bot: LanguageModel, bot_language: str,
                 translator: Translator):
        self._user = user
        self._user_language = user_language
        self._bot = bot
        self._bot_language = bot_language
        self._translator = translator
        if "history" not in st.session_state:
            st.session_state["history"] = []
        self._interactions = st.session_state["history"]

    def _send_message(self, prompt: str) -> Interaction:
        translated_prompt = self._translator.translate(
            prompt,
            from_language=self._user_language,
            to_language=self._bot_language,
        )
        translated_response = self._bot.generate(translated_prompt)
        response = self._translator.translate(
            translated_response,
            from_language=self._user_language,
            to_language=self._bot_language,
        )

        docs = [prompt, translated_prompt, translated_response, response]
        interaction = Interaction(
            docs, self._user_language, self._bot_language
        )
        self._interactions.append(interaction.json())
        return interaction

    def start_interaction(self) -> Interaction | None:
        user_input = self._user.get_input()
        if not user_input:
            return None

        # streamlit rerender hack
        skip = False
        if len(self._interactions) > 0:
            last_input = self._interactions[-1]["user"][self._user_language]
            skip = user_input == last_input

        if not skip:
            return self._send_message(user_input)

    def interactions(self):
        return self._interactions[::-1]


def main():
    st.header("Chatterbox")

    db = storage.VectorStore(COHERE_API_KEY)
    db.connect()

    user = User()
    if st.checkbox("DEBUG Mode", value=True):
        model = mock.MockLanguageModel()
        bot = mock.MockLanguageModel()
    else:
        model = anthropic.Claude(ANTHROPIC_API_KEY)
        bot = anthropic.ClaudeChatBot(ANTHROPIC_API_KEY)
    translator = translate.Translator(model)

    cols = st.columns(2)
    with cols[0]:
        from_lang = st.text_input("From Language", "en")
    with cols[1]:
        to_lang = st.text_input("To Language", "fr")

    chatterbox = Chatterbox(
        user=user,
        user_language=from_lang,
        bot=bot,
        bot_language=to_lang,
        translator=translator,
    )
    with st.spinner():
        interaction = chatterbox.start_interaction()

    if interaction:
        db.save_interaction(interaction)

    view_native = st.checkbox("View in native language")
    language = from_lang if view_native else to_lang

    for i, interaction in enumerate(chatterbox.interactions()):
        chat_message(interaction["bot"][language], key=f"{i}")
        chat_message(interaction["user"][language], is_user=True, key=f"{i}_user")


if __name__ == "__main__":
    main()
