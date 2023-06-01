import streamlit as st

from vocava.llm import anthropic, mock
from vocava.service import LANGUAGES, Service

ANTHROPIC_API_KEY = st.secrets["anthropic_api_key"]


def main():
    st.title('Translation')

    if st.sidebar.checkbox("DEBUG Mode", value=True):
        model = mock.MockLanguageModel()
    else:
        model = anthropic.Claude(ANTHROPIC_API_KEY)
    translator = Service("translator", model)

    from_lang = st.sidebar.selectbox("From Language", options=LANGUAGES)
    to_lang = st.sidebar.selectbox("To Language", options=LANGUAGES, index=4)

    text_to_translate = st.text_area("Enter text to translate")
    if st.button("Translate"):
        with st.spinner():
            data = translator.run(
                native_language=LANGUAGES[from_lang]["name"],
                target_language=LANGUAGES[to_lang]["name"],
                text=text_to_translate,
            )
        st.divider()

        translation = data["translation"]
        explanation = data["explanation"]
        st.text_area("Translated Text", translation)
        st.info(explanation)


if __name__ == "__main__":
    main()
