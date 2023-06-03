import streamlit as st

from vocava import entity

with open("home-page.md") as file:
    content = file.read()

st.title("Welcome to ***:violet[Vocava]*** 🚀")

st.markdown("""
Welcome to ***:violet[Vocava]*** 👋 your personal language learning sidekick!
No more humdrum textbooks or repetitive flashcards, ***:violet[Vocava]*** is your
personal tutor, here to transform your language conquest into a joyride 🎢 of laughter 
and discovery!

Ready to say "hola" to Spanish, or "こんにちは" to Japanese?
🌟 Harnessing the power of cutting-edge language models, ***:violet[Vocava]***
offers a fantastic blend of **:orange[time-tested]** language learning methods
and exciting advances in **:green[AI-driven]** techniques.
Picture this:
- your personal language tutor 🧑‍🏫
- an imaginative storyteller 📚
- an enthralling gaming arcade 🕹️
- a globe-trotting cultural guide 🌎
- and **:red[MORE]**, all in one place. ✅

So, buckle up, language adventurers! Let's explore the world of languages with 
***:violet[Vocava]*** 💫
""")

with st.expander("User Preferences"):
    st.markdown("You can setup your language preferences ⚙️ here.")
    st.info("Don't worry, you'll be able to change these in the sidebar "
            "later if you need to! 👍")
    languages = list(entity.LANGUAGES)
    default_native_lang = st.session_state.get("user.native_lang", languages[0])
    default_target_lang = st.session_state.get("user.target_lang", languages[4])
    default_fluency = st.session_state.get("user.fluency", 3)
    cols = st.columns(2)
    with cols[0]:
        native_language = st.selectbox(
            "Native Language", options=entity.LANGUAGES,
            index=languages.index(default_native_lang),
        )
    with cols[1]:
        target_language = st.selectbox(
            "Target Language", options=entity.LANGUAGES,
            index=languages.index(default_target_lang),
        )
    fluency = st.slider("Fluency", min_value=1, max_value=10, step=1,
                        value=default_fluency)
