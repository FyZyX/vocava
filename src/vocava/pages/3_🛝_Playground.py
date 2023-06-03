import random

import streamlit as st

from vocava import entity, service, storage

ANTHROPIC_API_KEY = st.secrets["anthropic_api_key"]
COHERE_API_KEY = st.secrets["cohere_api_key"]


def _generate_new_translations(user: entity.User, tutor: entity.Tutor):
    cols = st.columns(3)
    with cols[1]:
        start = st.button("Generate New Phrases")
    if start:
        practice_service = service.Service(
            name="playground-generate-translation-practice",
            user=user,
            tutor=tutor,
            max_tokens=500,
        )
        with st.spinner():
            data = practice_service.run(
                fluency=user.fluency(),
                known_phrases=user.known_phrases(),
            )
        st.session_state["translation.new"] = data["exercises"]
        st.session_state["translation.index"] = 0

    translations = st.session_state.get("translation.new", [])
    current_index = st.session_state.get("translation.index", 0)
    if not translations:
        return

    item = translations[current_index]
    phrase = item[user.target_language_name()]
    translation = item[user.native_language_name()]

    _, col, _ = st.columns([1, 3, 1])
    with col:
        st.subheader(f"*:orange[{phrase}]*")
    st.divider()
    cols = st.columns([1, 2, 3, 2, 2])
    with cols[1]:
        if st.button("< Previous"):
            prev_index = max(0, current_index - 1)
            st.session_state["translation.index"] = prev_index
            st.experimental_rerun()
    with cols[2]:
        show_answer = st.button("Show Translation", key=current_index)
    with cols[3]:
        save = st.button("Save")
    with cols[4]:
        if st.button("Next >"):
            next_index = min(len(translations) - 1, current_index + 1)
            st.session_state["translation.index"] = next_index
            st.experimental_rerun()

    if show_answer:
        st.success(translation)

    if save:
        with st.spinner():
            user.add_translation(phrase, translation)
        st.session_state["translation.new"].pop(current_index)
        st.session_state["translation.index"] = 0
        st.experimental_rerun()


def _review_translations(user: entity.User):
    cols = st.columns(3)
    with cols[1]:
        start = st.button("Study New Batch")
    if start:
        with st.spinner():
            known_phrases = user.known_phrases()
            if len(known_phrases) >= 10:
                phrases = random.choices(known_phrases, k=10)
            else:
                phrases = known_phrases
        st.session_state["translations.review"] = phrases
        st.session_state["translations.review.index"] = 0

    phrases = st.session_state.get("translations.review", [])
    current_index = st.session_state.get("translations.review.index", 0)
    if not phrases:
        return

    item = phrases[current_index]
    word = item[user.target_language_name()]
    translations = item[user.native_language_name()]
    if isinstance(translations, list):
        translations = ", ".join(item[user.native_language_name()])

    _, col, _ = st.columns([1, 3, 1])
    with col:
        st.header(f"*:orange[{word}]*")
    st.divider()
    cols = st.columns([1, 2, 3, 2])
    with cols[1]:
        if st.button("< Previous", key="review-prev"):
            prev_index = max(0, current_index - 1)
            st.session_state["translations.review.index"] = prev_index
            st.experimental_rerun()
    with cols[2]:
        show_answer = st.button("Show Translation", key=f"review-{current_index}")
    with cols[3]:
        if st.button("Next >", key="review-next"):
            next_index = min(len(phrases) - 1, current_index + 1)
            st.session_state["translations.review.index"] = next_index
            st.experimental_rerun()

    if show_answer:
        st.success(translations)


def translation_practice(user: entity.User, tutor: entity.Tutor):
    tabs = st.tabs(["Add New Phrases", "Review Phrases"])

    with tabs[0]:
        _generate_new_translations(user, tutor)

    with tabs[1]:
        _review_translations(user)


def _generate_new_vocabulary(user: entity.User, tutor: entity.Tutor):
    cols = st.columns(3)
    with cols[1]:
        start = st.button("Generate New Words")
    if start:
        practice_service = service.Service(
            name="playground-generate-vocabulary-practice",
            user=user,
            tutor=tutor,
            max_tokens=500,
        )
        with st.spinner():
            known_vocabulary = user.known_vocabulary()
            data = practice_service.run(
                fluency=user.fluency(),
                known_vocabulary=known_vocabulary,
            )
        st.session_state["vocabulary.new"] = data["vocabulary"]
        st.session_state["vocabulary.index"] = 0

    vocabulary = st.session_state.get("vocabulary.new", [])
    current_index = st.session_state.get("vocabulary.index", 0)
    if not vocabulary:
        return

    item = vocabulary[current_index]
    word = item[user.target_language_name()]
    translations = item[user.native_language_name()]
    if isinstance(translations, list):
        translations = ", ".join(item[user.native_language_name()])

    _, col, _ = st.columns([1, 3, 1])
    with col:
        st.header(f"*:blue[{word}]*")
    st.divider()
    cols = st.columns([1, 2, 3, 2, 2])
    with cols[1]:
        if st.button("< Previous"):
            prev_index = max(0, current_index - 1)
            st.session_state["vocabulary.index"] = prev_index
            st.experimental_rerun()
    with cols[2]:
        show_answer = st.button("Show Translation", key=current_index)
    with cols[3]:
        save = st.button("Save")
    with cols[4]:
        if st.button("Next >"):
            next_index = min(len(vocabulary) - 1, current_index + 1)
            st.session_state["vocabulary.index"] = next_index
            st.experimental_rerun()

    if show_answer:
        st.success(translations)

    if save:
        with st.spinner():
            user.add_vocabulary_word(word, translations)
        st.session_state["vocabulary.new"].pop(current_index)
        st.session_state["vocabulary.index"] = 0
        st.experimental_rerun()


def _review_known_vocabulary(user: entity.User):
    cols = st.columns(3)
    with cols[1]:
        start = st.button("Study New Batch")
    if start:
        with st.spinner():
            known_vocabulary = user.known_vocabulary()
            if len(known_vocabulary) >= 10:
                vocabulary = random.choices(known_vocabulary, k=10)
            else:
                vocabulary = known_vocabulary
        st.session_state["vocabulary.review"] = vocabulary
        st.session_state["vocabulary.review.index"] = 0

    vocabulary = st.session_state.get("vocabulary.review", [])
    current_index = st.session_state.get("vocabulary.review.index", 0)
    if not vocabulary:
        return

    item = vocabulary[current_index]
    word = item[user.target_language_name()]
    translations = item[user.native_language_name()]
    if isinstance(translations, list):
        translations = ", ".join(item[user.native_language_name()])

    _, col, _ = st.columns([1, 3, 1])
    with col:
        st.header(f"*:blue[{word}]*")
    st.divider()
    cols = st.columns([1, 2, 3, 2])
    with cols[1]:
        if st.button("< Previous", key="review-prev"):
            prev_index = max(0, current_index - 1)
            st.session_state["vocabulary.review.index"] = prev_index
            st.experimental_rerun()
    with cols[2]:
        show_answer = st.button("Show Translation", key=f"review-{current_index}")
    with cols[3]:
        if st.button("Next >", key="review-next"):
            next_index = min(len(vocabulary) - 1, current_index + 1)
            st.session_state["vocabulary.review.index"] = next_index
            st.experimental_rerun()

    if show_answer:
        st.success(translations)


def vocabulary_practice(user: entity.User, tutor: entity.Tutor):
    tabs = st.tabs(["Add New Words", "Review Words"])

    with tabs[0]:
        _generate_new_vocabulary(user, tutor)

    with tabs[1]:
        _review_known_vocabulary(user)


def _generate_new_grammar(user: entity.User, tutor: entity.Tutor):
    cols = st.columns([1, 2, 1])
    with cols[1]:
        start = st.button("Generate New Grammar Mistakes")
    if start:
        practice_service = service.Service(
            name="playground-generate-grammar-practice",
            user=user,
            tutor=tutor,
            max_tokens=500,
        )
        with st.spinner():
            data = practice_service.run(
                fluency=user.fluency(),
                known_phrases=user.known_mistakes(),
            )
        st.session_state["grammar.new"] = data["grammar"]
        st.session_state["grammar.index"] = 0

    mistakes = st.session_state.get("grammar.new", [])
    current_index = st.session_state.get("grammar.index", 0)
    if not mistakes:
        return

    item = mistakes[current_index]
    phrase = item["mistake"]
    correct = item["correct"]
    translation = item["translation"]
    explanation = item["explanation"]

    _, col, _ = st.columns([1, 3, 1])
    with col:
        st.subheader(f"*:green[{phrase}]*")
    st.divider()
    cols = st.columns([1, 2, 3, 2, 2])
    with cols[1]:
        if st.button("< Previous"):
            prev_index = max(0, current_index - 1)
            st.session_state["grammar.index"] = prev_index
            st.experimental_rerun()
    with cols[2]:
        show_answer = st.button("Show Correction", key=current_index)
    with cols[3]:
        save = st.button("Save")
    with cols[4]:
        if st.button("Next >"):
            next_index = min(len(mistakes) - 1, current_index + 1)
            st.session_state["grammar.index"] = next_index
            st.experimental_rerun()

    if show_answer:
        cols = st.columns(2)
        with cols[0]:
            st.success(correct)
        with cols[1]:
            st.warning(translation)
        st.info(explanation)

    if save:
        with st.spinner():
            user.add_grammar_mistake(phrase, correct, translation, explanation)
        st.session_state["grammar.new"].pop(current_index)
        st.session_state["grammar.index"] = 0
        st.experimental_rerun()


def _review_grammar(user: entity.User):
    cols = st.columns(3)
    with cols[1]:
        start = st.button("Study New Batch")
    if start:
        with st.spinner():
            known_mistakes = user.known_mistakes()
            if len(known_mistakes) >= 10:
                mistakes = random.choices(known_mistakes, k=10)
            else:
                mistakes = known_mistakes
        st.session_state["grammar.review"] = mistakes
        st.session_state["grammar.review.index"] = 0

    mistakes = st.session_state.get("grammar.review", [])
    current_index = st.session_state.get("grammar.review.index", 0)
    if not mistakes:
        return

    item = mistakes[current_index]
    phrase = item["mistake"]
    correct = item["correct"]
    translation = item["translation"]
    explanation = item["explanation"]

    _, col, _ = st.columns([1, 3, 1])
    with col:
        st.subheader(f"*:green[{phrase}]*")
    st.divider()
    cols = st.columns([1, 2, 3, 2])
    with cols[1]:
        if st.button("< Previous", key="review-prev"):
            prev_index = max(0, current_index - 1)
            st.session_state["grammar.review.index"] = prev_index
            st.experimental_rerun()
    with cols[2]:
        show_answer = st.button("Show Correction", key=f"review-{current_index}")
    with cols[3]:
        if st.button("Next >", key="review-next"):
            next_index = min(len(mistakes) - 1, current_index + 1)
            st.session_state["grammar.review.index"] = next_index
            st.experimental_rerun()

    if show_answer:
        cols = st.columns(2)
        with cols[0]:
            st.success(correct)
        with cols[1]:
            st.warning(translation)
        st.info(explanation)

def grammar_practice(user: entity.User, tutor: entity.Tutor):
    tabs = st.tabs(["Add New Grammar Mistakes", "Review Grammar Mistakes"])

    with tabs[0]:
        _generate_new_grammar(user, tutor)

    with tabs[1]:
        _review_grammar(user)


def main():
    st.title('Playground')

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
