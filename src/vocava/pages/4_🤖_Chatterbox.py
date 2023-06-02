import io
import json
import time

import openai
import streamlit as st
from streamlit_chat import message as chat_message

from vocava import storage
from vocava.llm import anthropic, mock, LanguageModel
from vocava.llm.prompt import load_prompt
from vocava.st_custom_components import st_audiorec
from vocava.service import LANGUAGES, Service

ANTHROPIC_API_KEY = st.secrets["anthropic_api_key"]
COHERE_API_KEY = st.secrets["cohere_api_key"]
openai.api_key = st.secrets["openai_api_key"]


class User:
    def __init__(self, fluency):
        self._fluency = fluency

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

    def get_input(self, input_method):
        if input_method == "Text Input":
            return self._get_text()
        elif input_method == "Voice Input":
            return self._get_audio_transcript()

    def fluency(self):
        return self._fluency


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
                 bot: LanguageModel, bot_language: str):
        self._user = user
        self._user_language = user_language
        self._bot = bot
        self._bot_language = bot_language
        if "history" not in st.session_state:
            st.session_state["history"] = []
        self._interactions = st.session_state["history"]

    def _send_message(
            self, message: str, native_mode: bool
    ) -> tuple[Interaction, str | None, str | None]:
        template = "chatterbox-native" if native_mode else "chatterbox-target"
        prompt = load_prompt(
            template,
            native_language=self._user_language,
            target_language=self._bot_language,
            fluency=self._user.fluency(),
            conversation_history=self._interactions,
            message=message,
        )
        response = self._bot.generate(prompt, max_tokens=5_000)
        try:
            start = response.find("{")
            payload = response[start:]
            data = json.loads(payload)
            return self._add_to_history(data)
        except json.decoder.JSONDecodeError:
            st.write(response)

    def _add_to_history(self, data) -> tuple[Interaction, str | None, str | None]:
        corrected = data["interaction"]["user"].get(f"{self._bot_language}_corrected")
        explanation = data["interaction"]["user"].get(
            f"{self._user_language}_explanation")
        docs = [
            data["interaction"]["user"][self._user_language],
            corrected or data["interaction"]["user"][self._bot_language],
            data["interaction"]["bot"][self._bot_language],
            data["interaction"]["bot"][self._user_language],
        ]
        interaction = Interaction(
            docs, self._user_language, self._bot_language
        )
        self._interactions.append(interaction.json())
        return interaction, corrected, explanation

    def start_interaction(
            self, user_input, native_mode: bool
    ) -> tuple[Interaction, str | None, str | None] | tuple[None, None, None]:
        # streamlit rerender hack
        skip = False
        if len(self._interactions) > 0:
            last_input = self._interactions[-1]["user"][self._user_language]
            skip = user_input == last_input

        if not skip:
            return self._send_message(user_input, native_mode)
        return None, None, None

    def interactions(self):
        return self._interactions[::-1]


def main():
    st.header("Chatterbox")

    db = storage.VectorStore(COHERE_API_KEY)
    db.connect()

    if st.sidebar.checkbox("DEBUG Mode", value=True):
        bot = mock.MockLanguageModel()
    else:
        bot = anthropic.ClaudeChatBot(ANTHROPIC_API_KEY)

    native_language = st.sidebar.selectbox("Native Language", options=LANGUAGES)
    target_language = st.sidebar.selectbox(
        "Choose Language", options=LANGUAGES, index=4)
    native_language_name = LANGUAGES[native_language]["name"]
    target_language_name = LANGUAGES[target_language]["name"]
    fluency = st.sidebar.slider("Fluency", min_value=1, max_value=10, step=1)

    input_method = st.sidebar.radio("Input method", ("Text Input", "Voice Input"))
    view_native = st.sidebar.checkbox("View in native language")

    user = User(fluency)
    chatterbox = Service(
        name="chatterbox",
        native_language=native_language_name,
        target_language=target_language_name,
        model=bot,
        max_tokens=150,
    )
    chatterbox = Chatterbox(
        user=user,
        user_language=native_language_name,
        bot=bot,
        bot_language=target_language_name,
    )
    user_input = user.get_input(input_method)
    if st.button("Send"):
        with st.spinner():
            interaction, corrected, explanation = chatterbox.start_interaction(
                user_input, native_mode=view_native)

        if interaction:
            db.save_interaction(interaction)
    else:
        interaction, corrected, explanation = None, None, None

    if corrected:
        st.warning(corrected)
        st.info(explanation)

    language = native_language_name if view_native else target_language_name
    for i, interaction in enumerate(chatterbox.interactions()):
        chat_message(interaction["bot"][language], key=f"{i}")
        chat_message(interaction["user"][language], is_user=True, key=f"{i}_user")


if __name__ == "__main__":
    main()
