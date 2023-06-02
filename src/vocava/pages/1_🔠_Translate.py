import streamlit as st

from vocava import entity, service

ANTHROPIC_API_KEY = st.secrets["anthropic_api_key"]


def main():
    st.title('Translation')

    debug_mode = st.sidebar.checkbox("DEBUG Mode", value=True)
    model = "Claude" if not debug_mode else "mock"
    tutor = entity.get_tutor(model, key=ANTHROPIC_API_KEY)

    from_lang = st.sidebar.selectbox("From Language", options=entity.LANGUAGES)
    to_lang = st.sidebar.selectbox("To Language", options=entity.LANGUAGES, index=4)
    fluency = st.sidebar.slider("Fluency", min_value=1, max_value=10, step=1)
    user = entity.User(
        native_language=from_lang,
        target_language=to_lang,
        fluency=fluency,
    )
    text = st.text_area("Enter text to translate")
    translator = service.Service(
        name="translator",
        user=user,
        tutor=tutor,
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
