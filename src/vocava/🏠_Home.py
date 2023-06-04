import pathlib
import sys

import streamlit as st

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from vocava import audio, entity


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

st.header("Language Preferences ⚙️")
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
st.info("Don't worry, you'll be able to change these in the sidebar "
        "later if you need to! 👍")

st.header("Activities 🥇")

expander = st.expander("Translation 📝")
expander.markdown("""
The :red[Translation] module allows you to translate text from your native language to 
your target language. The translated text also comes with a detailed explanation,
supporting your language learning journey.

[Visit Translation](/Translate)
""")

expander = st.expander("Storytime 📚")
expander.markdown("""
The :orange[Storyteller] module helps you improve language skills through storytelling.
Provide a concept, and our language model will generate a unique story around it.
You also receive comprehension questions related to the story, enhancing your
understanding of the target language.

[Visit Storytime](/Storytime)
""")

expander = st.expander("Playground 🛝")
expander.markdown("""
The :green[Playground] module offers a platform to practice and refine your language 
skills. Dive into various activities ranging from translation to vocabulary and grammar
practice.

[Visit Playground](/Playground)
""")

expander = st.expander("Chatterbox 🤖")
expander.markdown("""
In the :blue[Chatterbox] module, engage in an interactive chat with a language model 
tutor in your chosen target language. Get instant feedback on your inputs, making
real-time learning easier.

[Visit Chatterbox](/Chatterbox)
""")

expander = st.expander("Newsfeed 📰")
expander.markdown("""
Fetch, view, and translate news articles based on your specific interests in the
:violet[Newsfeed] module. This immersion in real-world context enhances your language
learning experience.

[Visit Newsfeed](/Newsfeed) 
""")

expander = st.expander("Arcade 🕹")
expander.markdown("""
Add a dash of fun to your learning with the :red[Arcade] module. Play games like
Jeopardy, Pictionary, MadLibs, and Odd One Out, all while improving your vocabulary
and fluency.

[Visit Arcade](/Arcade)
""")

expander = st.expander("Culture Corner 💃")
expander.markdown("""
Gain comprehensive cultural information with the :orange[Culture Corner] module.
Whether you want to create a cultural guide, plan a trip, or learn about
cultural faux pas in different regions, this module provides it all.

[Visit Culture Corner](/Culture_Corner)
""")

if "voices" not in st.session_state:
    with st.spinner():
        data = audio.get_voices()
    st.session_state["voices"] = dict([
        (voice.name, voice.voice_id)
        for voice in data
    ])
