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

    from_lang = st.sidebar.selectbox("From Language", options=LANGUAGES)
    to_lang = st.sidebar.selectbox("To Language", options=LANGUAGES, index=4)
    text = st.text_area("Enter text to translate")
    translator = Service(
        name="translator",
        native_language=from_lang,
        target_language=to_lang,
        model=model,
        max_tokens=len(text) + 50,
    )
    if st.button("Translate"):
        with st.spinner():
            data = translator.run(text=text)
        st.divider()

        translation = data["translation"]
        explanation = data["explanation"]
        st.text_area("Translated Text", translation)
        st.info(explanation)


if __name__ == "__main__":
    main()
