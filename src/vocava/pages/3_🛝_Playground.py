import json

import streamlit as st

from vocava.llm import LanguageModel, anthropic, mock
from vocava.llm.prompt import load_prompt
from vocava.translate import LANGUAGES

ANTHROPIC_API_KEY = st.secrets["anthropic_api_key"]


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
            st.write(data)


if __name__ == "__main__":
    main()
