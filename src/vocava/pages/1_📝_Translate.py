import streamlit as st

from vocava import entity, service

ANTHROPIC_API_KEY = st.secrets["anthropic_api_key"]


def main():
    st.title('Translation')

    tutor = entity.get_tutor("Claude", key=ANTHROPIC_API_KEY)

    languages = list(entity.LANGUAGES)
    default_native_lang = st.session_state.get("user.native_lang", languages[0])
    default_target_lang = st.session_state.get("user.target_lang", languages[4])
    default_fluency = st.session_state.get("user.fluency", 3)
    native_language = st.sidebar.selectbox(
        "Native Language", options=entity.LANGUAGES,
        index=languages.index(default_native_lang),
    )
    target_language = st.sidebar.selectbox(
        "Choose Language", options=entity.LANGUAGES,
        index=languages.index(default_target_lang),
    )

    fluency = st.sidebar.slider("Fluency", min_value=1, max_value=10, step=1,
                                value=default_fluency)
    user = entity.User(
        native_language=native_language,
        target_language=target_language,
        fluency=fluency,
    )
    st.session_state["user.native_lang"] = native_language
    st.session_state["user.target_lang"] = target_language
    st.session_state["user.fluency"] = fluency

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
