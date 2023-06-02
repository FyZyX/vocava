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
    def __init__(self, user: entity.User, user_language: str,
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

    if st.button("Send"):
        chatterbox = Service(
            name="chatterbox",
            user=user,
            tutor=tutor,
            max_tokens=150,
            native_mode=view_native,
        )
        with st.spinner():
            interaction, corrected, explanation = chatterbox.run(message=user_input)

        if interaction:
            db.save_interaction(interaction)
    else:
        interaction, corrected, explanation = None, None, None

    if corrected:
        st.warning(corrected)
        st.info(explanation)

    language = chatterbox.current_language()
    for i, interaction in enumerate(chatterbox.interactions()):
        chat_message(interaction["bot"][language], key=f"{i}")
        chat_message(interaction["user"][language], is_user=True, key=f"{i}_user")


if __name__ == "__main__":
    main()
