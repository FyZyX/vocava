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

    def generate_story(self, language: str, fluency: int,
                       concept: str) -> dict[str, Any]:
        prompt = load_prompt(
            "storytime-generate",
            language=language,
            fluency=fluency,
            concept=concept,
        )
        response = self._model.generate(prompt, max_tokens=1_000)
        try:
            return json.loads(response)
        except json.decoder.JSONDecodeError:
            st.write(response)


def main():
    st.title('Storyteller')

    if st.sidebar.checkbox("DEBUG Mode", value=True):
        model = mock.MockLanguageModel()
    else:
        model = anthropic.Claude(ANTHROPIC_API_KEY)

    language = st.sidebar.selectbox("Choose Language", options=LANGUAGES, index=12)
    fluency = st.sidebar.slider("Fluency", min_value=1, max_value=10, step=1)

    user_prompt = st.text_input("What kind of story would you like?")
    if st.button("Generate Story"):
        storyteller = Storyteller(model)
        with st.spinner():
            data = storyteller.generate_story(language, fluency, user_prompt)
        generated_story = data["story"]
        comprehension_questions = data["questions"]
        st.markdown(generated_story)
        for i, item in enumerate(comprehension_questions):
            st.write(item["question"])
            if st.checkbox("Show Answer", key=f"q{i}"):
                st.success(item["answer"])


if __name__ == "__main__":
    main()
