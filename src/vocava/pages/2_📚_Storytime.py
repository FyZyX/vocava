import streamlit as st

from vocava.llm import anthropic, mock
from vocava.service import LANGUAGES, Service

ANTHROPIC_API_KEY = st.secrets["anthropic_api_key"]


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
    view_native = st.sidebar.checkbox("View in native language")

    concept = st.text_input("What kind of story would you like?")
    storytime = Service(
        "storytime",
        native_language=native_language,
        target_language=target_language,
        native_mode=view_native,
        model=model,
        max_tokens=1_000,
    )
    if st.button("Generate Story"):
        with st.spinner():
            data = storytime.run(fluency=fluency, concept=concept)
        st.session_state["data"] = data

    language = storytime.current_language()
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
