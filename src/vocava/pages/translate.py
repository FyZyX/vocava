import pathlib
import sys

import openai
import streamlit as st

from vocava.llm import LanguageModel, anthropic, mock

ANTHROPIC_API_KEY = st.secrets["anthropic_api_key"]
COHERE_API_KEY = st.secrets["cohere_api_key"]
openai.api_key = st.secrets["openai_api_key"]


class Translator:
    def __init__(self, model: LanguageModel):
        self._model = model

    def translate(self, text: str, from_language, to_language) -> str:
        prompt = f"Translate the TEXT from {from_language} to {to_language}\n" \
                 f"TEXT:\n\"{text}\""
        return self._model.generate(prompt)


def translation_page():
    st.title('Translation')

    col1, col2 = st.columns(2)
    from_lang = col1.text_input("From Language", "en")
    to_lang = col2.text_input("To Language", "fr")

    text_to_translate = st.text_area("Enter text to translate")
    if st.button("Translate"):
        # model = anthropic.Claude(ANTHROPIC_API_KEY)
        model = mock.MockLanguageModel()
        translator = Translator(model)
        with st.spinner():
            translated_text = translator.translate(text_to_translate, from_lang, to_lang)
        st.divider()
        st.text_area("Translated Text", translated_text)


if __name__ == "__main__":
    sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
    translation_page()
