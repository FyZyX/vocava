import json

import streamlit as st

from vocava.llm import LanguageModel, anthropic, mock
from vocava.llm.prompt import load_prompt
from vocava.translate import LANGUAGES

ANTHROPIC_API_KEY = st.secrets["anthropic_api_key"]
USER_VOCABULARY = {
    "Japanese": {
        "はじめまして": ["How do you do?", "Nice to meet you"],
        "うれしい": ["happy", "glad", "joyful"],
        "つくづく": ["really", "indeed"],
        "ストーブ": ["stove"],
        "さすがに": ["as expected", "sure enough"],
        "ありゃありゃ": ["my my", "dear me"],
        "あざとい": ["showy", "flashy", "gaudy"],
        "ohayou gozaimasu": ["good morning", "hello"],
        "konnichiwa": ["good day", "hello"],
        "oyasumi nasai": ["good night"],
        "sumimasen": ["excuse me"],
        "arigatou gozaimasu": ["thank you"],
        "nani o shimasu ka": ["what are you doing?"],
        "sore wa totemo oishii desu": ["that is very tasty"],
    }
}


class Playground:
    def __init__(self, model: LanguageModel):
        self._model = model

    def generate_translation_practice(self, native_language, target_language, fluency):
        prompt = load_prompt(
            "playground-generate-translation-practice",
            native_language=native_language,
            target_language=target_language,
            fluency=fluency,
        )
        response = self._model.generate(prompt, max_tokens=500)
        try:
            start = response.find("{")
            payload = response[start:]
            return json.loads(payload)
        except json.decoder.JSONDecodeError:
            st.write(response)

    def generate_vocabulary_practice(self, native_language, target_language,
                                     fluency, known_vocabulary):
        prompt = load_prompt(
            "playground-generate-vocabulary-practice",
            native_language=native_language,
            target_language=target_language,
            fluency=fluency,
            known_vocabulary=known_vocabulary,
        )
        response = self._model.generate(prompt, max_tokens=500)
        try:
            start = response.find("{")
            payload = response[start:]
            return json.loads(payload)
        except json.decoder.JSONDecodeError:
            st.write(response)


def main():
    st.title('Playground')

    if st.sidebar.checkbox("DEBUG Mode", value=True):
        model = mock.MockLanguageModel()
    else:
        model = anthropic.Claude(ANTHROPIC_API_KEY)

    native_language = st.sidebar.selectbox("Native Language", options=LANGUAGES)
    target_language = st.sidebar.selectbox(
        "Choose Language", options=LANGUAGES, index=12)
    native_language_name = LANGUAGES[native_language]["name"]
    target_language_name = LANGUAGES[target_language]["name"]
    fluency = st.sidebar.slider("Fluency", min_value=1, max_value=10, step=1)

    playground = Playground(model)
    activities = [
        "Translation Practice",
        "Vocabulary Practice",
    ]
    activity = st.selectbox("Choose an activity", activities)
    if activity == "Translation Practice":
        if st.button("Start"):
            with st.spinner():
                data = playground.generate_translation_practice(
                    native_language=native_language_name,
                    target_language=target_language_name,
                    fluency=fluency,
                )
            st.session_state["exercises"] = data["exercises"]
        vocabulary = st.session_state.get("exercises", [])
        for i, phrase in enumerate(vocabulary):
            cols = st.columns(2)
            with cols[0]:
                st.write(phrase[target_language_name])
            with cols[1]:
                show_answer = st.checkbox("Show Answer", key=i)
            if show_answer:
                st.success(phrase[native_language_name])
    elif activity == "Vocabulary Practice":
        if st.button("Start"):
            with st.spinner():
                data = playground.generate_vocabulary_practice(
                    native_language=native_language_name,
                    target_language=target_language_name,
                    fluency=fluency,
                    known_vocabulary=USER_VOCABULARY.get(target_language_name, []),
                )
            st.session_state["vocabulary"] = data["vocabulary"]
        vocabulary = st.session_state.get("vocabulary", [])
        for i, phrase in enumerate(vocabulary):
            cols = st.columns([2, 1])
            with cols[0]:
                st.write(phrase[target_language_name])
            with cols[1]:
                show_answer = st.checkbox("Show Answer", key=i)
            if show_answer:
                translations = phrase[native_language_name]
                if isinstance(translations, list):
                    st.success(", ".join(phrase[native_language_name]))
                else:
                    st.success(translations)


if __name__ == "__main__":
    main()
