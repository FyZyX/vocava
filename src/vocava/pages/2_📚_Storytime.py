import json
from typing import Any

import streamlit as st

from vocava.llm import LanguageModel, anthropic, mock
from vocava.llm.prompt import load_prompt
from vocava.translate import LANGUAGES

ANTHROPIC_API_KEY = st.secrets["anthropic_api_key"]


class Storyteller:
    def __init__(self, model: LanguageModel):
        self._model = model

    def generate_story(self, native_language: str, target_language: str,
                       fluency: int, concept: str) -> dict[str, Any]:
        prompt = load_prompt(
            "storytime",
            native_language=native_language,
            target_language=target_language,
            fluency=fluency,
            concept=concept,
        )
        response = self._model.generate(prompt, max_tokens=2_000)
        try:
            start = response.find("{")
            payload = response[start:]
            return json.loads(payload)
        except json.decoder.JSONDecodeError:
            st.write(response)


def main():
    if "data" not in st.session_state:
        st.session_state["data"] = None

    st.title("Storyteller")

    if st.sidebar.checkbox("DEBUG Mode", value=True):
        model = mock.MockLanguageModel()
    else:
        model = anthropic.Claude(ANTHROPIC_API_KEY)

    native_language = st.sidebar.selectbox("Native Language", options=LANGUAGES)
    target_language = st.sidebar.selectbox("Choose Language", options=LANGUAGES,
                                           index=12)
    fluency = st.sidebar.slider("Fluency", min_value=1, max_value=10, step=1)
    show_native = st.sidebar.checkbox("View in native language")

    user_prompt = st.text_input("What kind of story would you like?")
    native_language_name = LANGUAGES[native_language]["name"]
    target_language_name = LANGUAGES[target_language]["name"]
    if st.button("Generate Story"):
        storyteller = Storyteller(model)
        with st.spinner():
            data = storyteller.generate_story(
                native_language_name,
                target_language_name,
                fluency,
                user_prompt,
            )
        st.session_state["data"] = data

    language = native_language_name if show_native else target_language_name
    data = st.session_state["data"]
    if not data or language not in data["story"]:
        return

    generated_story = st.session_state["data"]["story"][language]
    comprehension_questions = st.session_state["data"]["questions"]
    st.markdown(generated_story)
    for i, item in enumerate(comprehension_questions):
        cols = st.columns(2)
        with cols[0]:
            st.write(item[f"question_{language}"])
        with cols[1]:
            show_answer = st.checkbox("Show Answer", key=f"q{i}")
        if show_answer:
            st.success(item[f"answer_{language}"])


if __name__ == "__main__":
    main()
