import streamlit as st

from vocava.llm import anthropic, mock
from vocava.service import LANGUAGES, Service

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
USER_PHRASES = {
    "Japanese": {
    }
}


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

    activities = [
        "Translation Practice",
        "Vocabulary Practice",
        "Grammar Practice",
    ]
    activity = st.selectbox("Choose an activity", activities)
    if activity == "Translation Practice":
        if st.button("Start"):
            translation_practice = Service(
                name="playground-generate-translation-practice",
                native_language=native_language,
                target_language=target_language,
                model=model,
                max_tokens=500,
            )
            with st.spinner():
                data = translation_practice.run(fluency=fluency)
            st.session_state["exercises"] = data["exercises"]
        vocabulary = st.session_state.get("exercises", [])
        for i, grammar_item in enumerate(vocabulary):
            cols = st.columns(2)
            with cols[0]:
                st.write(grammar_item[target_language_name])
            with cols[1]:
                show_answer = st.checkbox("Show Answer", key=i)
            if show_answer:
                st.success(grammar_item[native_language_name])
    elif activity == "Vocabulary Practice":
        if st.button("Start"):
            vocabulary_practice = Service(
                name="playground-generate-vocabulary-practice",
                native_language=native_language,
                target_language=target_language,
                model=model,
                max_tokens=500,
            )
            with st.spinner():
                data = vocabulary_practice.run(
                    native_language=native_language_name,
                    target_language=target_language_name,
                    fluency=fluency,
                    known_vocabulary=USER_VOCABULARY.get(target_language_name, []),
                )
            st.session_state["vocabulary"] = data["vocabulary"]
        vocabulary = st.session_state.get("vocabulary", [])
        for i, grammar_item in enumerate(vocabulary):
            cols = st.columns([2, 1])
            with cols[0]:
                st.write(grammar_item[target_language_name])
            with cols[1]:
                show_answer = st.checkbox("Show Answer", key=i)
            if show_answer:
                translations = grammar_item[native_language_name]
                if isinstance(translations, list):
                    st.success(", ".join(grammar_item[native_language_name]))
                else:
                    st.success(translations)
    elif activity == "Grammar Practice":
        if st.button("Start"):
            grammar_practice = Service(
                name="playground-generate-grammar-practice",
                native_language=native_language,
                target_language=target_language,
                model=model,
                max_tokens=500,
            )
            with st.spinner():
                data = grammar_practice.run(
                    native_language=native_language_name,
                    target_language=target_language_name,
                    fluency=fluency,
                    known_phrases=USER_PHRASES.get(target_language_name, []),
                )
            st.json(data)
            st.session_state["grammar"] = data["grammar"]
        vocabulary = st.session_state.get("grammar", [])
        for i, grammar_item in enumerate(vocabulary):
            cols = st.columns([2, 1])
            with cols[0]:
                st.write(grammar_item["mistake"])
            with cols[1]:
                show_answer = st.checkbox("Show Answer", key=i)
            if show_answer:
                corrected = grammar_item["correct"]
                translation = grammar_item["translation"]
                explanation = grammar_item["explanation"]
                st.success(corrected)
                st.warning(translation)
                st.info(explanation)


if __name__ == "__main__":
    main()
