import io

import openai
import streamlit as st

from vocava.st_custom_components import st_audiorec


def review_mistakes():
    # This could involve retrieving a list of common errors
    # the user has made from a database and displaying them.
    st.header("Your past mistakes:")
    mistakes = [
        "Mistake 1",
        "Mistake 2",
        "Mistake 3",
    ]  # Fetch these from your database
    for mistake in mistakes:
        st.markdown(mistake)


def word_reminders():
    # This could involve retrieving a list of words the user
    # is learning from a database and displaying them.
    st.header("Words to remember:")
    words = ["Word 1", "Word 2", "Word 3"]  # Fetch these from your database
    for word in words:
        st.markdown(word)


def grammar_lessons():
    # This could involve retrieving a list of grammar lessons
    # from a database and displaying them.
    st.header("Your grammar lessons:")
    lessons = ["Lesson 1", "Lesson 2", "Lesson 3"]  # Fetch these from your database
    for lesson in lessons:
        st.markdown(lesson)


def speech_exercise():
    st.header("Record your pronunciation:")
    wav_audio_data = st_audiorec()
    if wav_audio_data is not None:
        file = io.BytesIO(wav_audio_data)
        file.name = "tmp.wav"
        with st.spinner():
            response = openai.Audio.transcribe("whisper-1", file)
            st.text("Your speech transcription: " + response["text"])
            # Use your language model to provide feedback
            # on the user's pronunciation here


def playground_page():
    st.title('Playground')

    activities = {
        "Review Mistakes": review_mistakes,
        "Word Reminders": word_reminders,
        "Grammar Lessons": grammar_lessons,
        "Speech Exercise": speech_exercise,
    }
    activity = st.selectbox("Choose an activity", activities.keys())
    start_activity = activities.get(activity)

    start_activity()


if __name__ == "__main__":
    playground_page()
