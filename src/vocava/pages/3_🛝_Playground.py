import streamlit as st

from vocava import entity
from vocava.service import Service

ANTHROPIC_API_KEY = st.secrets["anthropic_api_key"]


def translation_practice(user: entity.User, tutor: entity.Tutor):
    if st.button("Start"):
        translation_practice = Service(
            name="playground-generate-translation-practice",
            user=user,
            tutor=tutor,
            max_tokens=500,
        )
        with st.spinner():
            data = translation_practice.run(fluency=user.fluency())
        st.session_state["exercises"] = data["exercises"]
    vocabulary = st.session_state.get("exercises", [])
    for i, grammar_item in enumerate(vocabulary):
        cols = st.columns(2)
        with cols[0]:
            st.write(grammar_item[user.target_language_name()])
        with cols[1]:
            show_answer = st.checkbox("Show Answer", key=i)
        if show_answer:
            st.success(grammar_item[user.native_language_name()])


def vocabular_practice(user: entity.User, tutor: entity.Tutor):
    if st.button("Start"):
        vocabulary_practice = Service(
            name="playground-generate-vocabulary-practice",
            user=user,
            tutor=tutor,
            max_tokens=500,
        )
        with st.spinner():
            data = vocabulary_practice.run(
                fluency=user.fluency(),
                known_vocabulary=user.known_vocabulary(),
            )
        st.session_state["vocabulary"] = data["vocabulary"]
    vocabulary = st.session_state.get("vocabulary", [])
    for i, grammar_item in enumerate(vocabulary):
        cols = st.columns([2, 1])
        with cols[0]:
            st.write(grammar_item[user.target_language_name()])
        with cols[1]:
            show_answer = st.checkbox("Show Answer", key=i)
        if show_answer:
            translations = grammar_item[user.native_language_name()]
            if isinstance(translations, list):
                st.success(", ".join(grammar_item[user.native_language_name()]))
            else:
                st.success(translations)


def grammar_practice(user: entity.User, tutor: entity.Tutor):
    if st.button("Start"):
        grammar_practice = Service(
            name="playground-generate-grammar-practice",
            user=user,
            tutor=tutor,
            max_tokens=500,
        )
        with st.spinner():
            data = grammar_practice.run(
                native_language=user.native_language_name(),
                target_language=user.target_language_name(),
                fluency=user.fluency(),
                known_phrases=user.known_phrases(),
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


def main():
    st.title('Playground')

    debug_mode = st.sidebar.checkbox("DEBUG Mode", value=True)
    model = "Claude" if not debug_mode else "mock"
    tutor = entity.get_tutor(model, key=ANTHROPIC_API_KEY)

    native_language = st.sidebar.selectbox("Native Language", options=entity.LANGUAGES)
    target_language = st.sidebar.selectbox(
        "Choose Language", options=entity.LANGUAGES, index=12)
    fluency = st.sidebar.slider("Fluency", min_value=1, max_value=10, step=1)
    user = entity.User(
        native_language=native_language,
        target_language=target_language,
        fluency=fluency,
    )

    activities = [
        "Translation Practice",
        "Vocabulary Practice",
        "Grammar Practice",
    ]
    activity = st.selectbox("Choose an activity", activities)
    if activity == "Translation Practice":
        translation_practice(user, tutor)
    elif activity == "Vocabulary Practice":
        vocabular_practice(user, tutor)
    elif activity == "Grammar Practice":
        grammar_practice(user, tutor)


if __name__ == "__main__":
    main()
