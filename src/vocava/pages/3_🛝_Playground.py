import streamlit as st

from vocava import entity, service, storage

ANTHROPIC_API_KEY = st.secrets["anthropic_api_key"]
COHERE_API_KEY = st.secrets["cohere_api_key"]


def translation_practice(user: entity.User, tutor: entity.Tutor):
    if st.button("Start"):
        practice_service = service.Service(
            name="playground-generate-translation-practice",
            user=user,
            tutor=tutor,
            max_tokens=500,
        )
        with st.spinner():
            data = practice_service.run(fluency=user.fluency())
        st.session_state["exercises"] = data["exercises"]
    exercises = st.session_state.get("exercises", [])
    for i, exercise in enumerate(exercises):
        cols = st.columns(2)
        with cols[0]:
            st.write(exercise[user.target_language_name()])
        with cols[1]:
            show_answer = st.checkbox("Show Answer", key=i)
        if show_answer:
            st.success(exercise[user.native_language_name()])


def vocabulary_practice(user: entity.User, tutor: entity.Tutor):
    known_vocabulary = user.known_vocabulary()
    st.warning(known_vocabulary["documents"])
    if st.button("Start"):
        practice_service = service.Service(
            name="playground-generate-vocabulary-practice",
            user=user,
            tutor=tutor,
            max_tokens=500,
        )
        with st.spinner():
            data = practice_service.run(
                fluency=user.fluency(),
                known_vocabulary=user.known_vocabulary(),
            )
        st.session_state["vocabulary"] = data["vocabulary"]
        st.session_state["current_index"] = 0

    vocabulary = st.session_state.get("vocabulary", [])
    current_index = st.session_state.get("current_index", 0)
    if not vocabulary:
        return

    word_item = vocabulary[current_index]
    word = word_item[user.target_language_name()]

    st.header(word)
    st.info(current_index)
    st.divider()
    cols = st.columns([1, 2, 2, 2])
    with cols[1]:
        if st.button("Previous"):
            prev_index = max(0, current_index - 1)
            st.session_state["current_index"] = prev_index
            st.experimental_rerun()
    with cols[2]:
        show_answer = st.button("Show Answer", key=current_index)
    with cols[3]:
        if st.button("Next"):
            next_index = min(len(vocabulary) - 1, current_index + 1)
            st.session_state["current_index"] = next_index
            st.experimental_rerun()

    if show_answer:
        translations = word_item[user.native_language_name()]
        if isinstance(translations, list):
            translations = ", ".join(word_item[user.native_language_name()])
        st.success(translations)

        if st.button("Save Word"):
            with st.spinner():
                user.add_vocabulary_word(word, translations)


def grammar_practice(user: entity.User, tutor: entity.Tutor):
    if st.button("Start"):
        practice_service = service.Service(
            name="playground-generate-grammar-practice",
            user=user,
            tutor=tutor,
            max_tokens=500,
        )
        with st.spinner():
            data = practice_service.run(
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
    store = storage.VectorStore(COHERE_API_KEY)
    store.connect()
    user = entity.User(
        native_language=native_language,
        target_language=target_language,
        fluency=fluency,
        db=store,
    )
    st.session_state["user.native_lang"] = native_language
    st.session_state["user.target_lang"] = target_language
    st.session_state["user.fluency"] = fluency

    activities = {
        "Translation Practice": translation_practice,
        "Vocabulary Practice": vocabulary_practice,
        "Grammar Practice": grammar_practice,
    }
    activity = st.selectbox("Choose an activity", activities)
    start_activity = activities.get(activity)
    start_activity(user, tutor)


if __name__ == "__main__":
    main()
