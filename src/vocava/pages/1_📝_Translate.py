import io

import elevenlabs
import openai
import streamlit as st
from annotated_text import annotated_text

from vocava import entity, service, storage
from vocava.st_custom_components import st_audiorec

ANTHROPIC_API_KEY = st.secrets["anthropic_api_key"]
COHERE_API_KEY = st.secrets["cohere_api_key"]
openai.api_key = st.secrets["openai_api_key"]
elevenlabs.set_api_key(st.secrets["eleven_labs_api_key"])


def get_audio_transcript():
    data = st_audiorec()
    if not data:
        return None

    file = io.BytesIO(data)
    file.name = "tmp.wav"
    with st.spinner():
        response = openai.Audio.transcribe("whisper-1", file)
    return response["text"]


def get_voices():
    return elevenlabs.voices()


def text_to_speech(text, voice_id):
    return elevenlabs.generate(
        text=text,
        voice=voice_id,
        model="eleven_multilingual_v1"
    )


def main():
    st.title("Translate")

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

    can_vocalize = target_language in entity.VOCALIZED_LANGUAGES
    if can_vocalize and "voices" not in st.session_state:
        with st.spinner():
            voices = get_voices()
        st.session_state["voices"] = dict([
            (voice.name, voice.voice_id)
            for voice in voices
        ])

    speech_input = st.sidebar.checkbox("Enable Input Audio")
    voices = st.session_state.get("voices")
    selected_voice = None
    if can_vocalize:
        synthesize = st.sidebar.checkbox("Enable Output Audio")
        if synthesize:
            selected_voice = st.sidebar.selectbox(
                "Output Voice", options=voices
            )

    if speech_input:
        text = get_audio_transcript()
    else:
        text = st.text_area("Enter text to translate")

    if st.button("Translate"):
        translator = service.Service(
            name="translate",
            user=user,
            tutor=tutor,
            max_tokens=6 * len(text) + 150,
        )
        with st.spinner():
            data = translator.run(text=text)
        st.session_state["translate"] = data

    data = st.session_state.get("translate")
    if not data or text != data:
        return

    translation = data["translation"]
    explanation = data["explanation"]

    st.divider()
    st.text_area("Translated Text", translation)
    if can_vocalize and selected_voice:
        if "translate.audio" not in st.session_state:
            with st.spinner():
                audio = text_to_speech(translation, voices[selected_voice])
            st.session_state["translate.audio"] = audio

        audio = st.session_state["translate.audio"]
        st.audio(audio, format='audio/mpeg')

    translation_tagged = [(item["word"], item["pos"])
                          for item in data["dictionary"]]
    tagged = [(item["original"], item["pos"]) for item in data["dictionary"]]
    st.divider()
    annotated_text(translation_tagged)
    st.divider()
    annotated_text(tagged)
    st.divider()
    st.info(explanation)


if __name__ == "__main__":
    main()
