import io
import time
from typing import Protocol

import anthropic
import chromadb
import cohere
import openai
import streamlit as st
from chromadb.utils import embedding_functions
from streamlit_chat import message as chat_message

from st_custom_components import st_audiorec

DEBUG = True
ANTHROPIC_API_KEY = st.secrets["anthropic_api_key"]
COHERE_API_KEY = st.secrets["cohere_api_key"]
openai.api_key = st.secrets["openai_api_key"]


class User:
    def get_text(self, default=""):
        return st.text_input("Enter a Message", default)


class LanguageModel(Protocol):
    def generate(self, prompt: str) -> str:
        pass


class ClaudeLanguageModel:
    def __init__(self, api_key: str):
        self._client = anthropic.Client(api_key=api_key)

    @staticmethod
    def _wrap_prompt(text):
        return anthropic.HUMAN_PROMPT + text + anthropic.AI_PROMPT

    def generate(self, prompt: str) -> str:
        if DEBUG:
            return "response message"
        return self._client.completion(
            prompt=self._wrap_prompt(prompt),
            stop_sequences=[anthropic.HUMAN_PROMPT],
            model="claude-v1.3-100k",
            max_tokens_to_sample=200,
        )["completion"]


class ClaudeChatBot(ClaudeLanguageModel):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self._history = ""

    def generate(self, prompt: str) -> str:
        self._history += self._wrap_prompt(prompt)
        response = self._client.completion(
            prompt=self._history,
            stop_sequences=[anthropic.HUMAN_PROMPT],
            model="claude-v1.3-100k",
            max_tokens_to_sample=200,
        )["completion"]
        self._history += response
        return response


class Translator:
    def __init__(self, model: LanguageModel):
        self._model = model

    def translate(self, text: str, from_language, to_language) -> str:
        prompt = f"Translate the TEXT from {from_language} to {to_language}\n" \
                 f"TEXT:\n\"{text}\""
        return self._model.generate(prompt)


class TranslationLanguageModel:
    def __init__(self, model: LanguageModel, translator: Translator,
                 native_language: str, target_language: str,
                 db: chromadb.Client):
        self._model = model
        self._translator = translator
        self._native_language = native_language
        self._target_language = target_language
        self._last_translation = None
        self._collection = db.get_or_create_collection(
            name="vocava",
            embedding_function=embedding_functions.CohereEmbeddingFunction(
                api_key=COHERE_API_KEY,
                model_name="embed-multilingual-v2.0",
            ),
        )

    def _interaction_ids(self):
        message_id = int(time.time())
        return [
            f"{message_id}-user-{self._native_language}",
            f"{message_id}-user-{self._target_language}",
            f"{message_id}-bot-{self._target_language}",
            f"{message_id}-bot-{self._native_language}",
        ]

    def _interaction_metadata(self):
        return [
            {"language": self._native_language},
            {"language": self._target_language},
            {"language": self._target_language},
            {"language": self._native_language},
        ]

    def _save(self, docs):
        self._collection.add(
            ids=self._interaction_ids(),
            documents=docs,
            metadatas=self._interaction_metadata(),
        )

    def last_translation(self):
        prompt, translated_prompt, translated_response, response = self._last_translation
        return {
            'user': {
                self._native_language: prompt,
                self._target_language: translated_prompt,
            },
            'bot': {
                self._target_language: translated_response,
                self._native_language: response,
            },
        }

    def generate(self, prompt: str) -> str:
        translated_prompt = self._translator.translate(
            prompt,
            from_language=self._native_language,
            to_language=self._target_language,
        )
        translated_response = self._model.generate(translated_prompt)
        response = self._translator.translate(
            translated_response,
            from_language=self._target_language,
            to_language=self._native_language,
        )

        docs = [prompt, translated_prompt, translated_response, response]
        self._save(docs)
        self._last_translation = docs
        return translated_response


def embed(docs: list[str]):
    cohere_client = cohere.Client(api_key=COHERE_API_KEY)
    return cohere_client.embed(texts=docs, model='embed-english')


def send_message(user_input, native_lang, target_lang, db):
    model = ClaudeLanguageModel(ANTHROPIC_API_KEY)
    translator = Translator(model)
    bot = ClaudeChatBot(ANTHROPIC_API_KEY)
    translation_bot = TranslationLanguageModel(
        bot, translator, native_lang, target_lang, db
    )

    completion = translation_bot.generate(user_input)

    st.session_state['history'].append(translation_bot.last_translation())
    return completion


def main():
    st.set_page_config(
        page_title="Vocava - Demo",
        page_icon=":robot:"
    )
    db = chromadb.Client()

    st.header("Vocava")

    col1, col2 = st.columns(2)
    native_lang = col1.text_input("Your native language: ", "en")
    target_lang = col2.text_input("Your target language: ", "fr")

    if 'history' not in st.session_state:
        st.session_state['history'] = []

    input_method = st.radio("Input method", ("Text Input", "Voice Input"))
    if input_method == "Text Input":
        user = User()
        user_input = user.get_text()
        if st.button("Send"):
            send_message(user_input, native_lang, target_lang, db)
    elif input_method == "Voice Input":
        wav_audio_data = st_audiorec()
        if wav_audio_data is not None:
            file = io.BytesIO(wav_audio_data)
            file.name = "tmp.wav"
            with st.spinner():
                response = openai.Audio.transcribe("whisper-1", file)
                user_input = response["text"]
                send_message(user_input, native_lang, target_lang, db)

    if st.session_state['history']:
        view_target = st.checkbox('View in target language')
        for i in range(len(st.session_state['history']) - 1, -1, -1):
            message = st.session_state["history"][i]
            language = target_lang if view_target else native_lang
            chat_message(message['bot'][language], key=f"{i}")
            chat_message(message['user'][language], is_user=True, key=f'{i}_user')


if __name__ == '__main__':
    main()
