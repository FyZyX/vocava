import io

import elevenlabs
import openai


def get_audio_transcript(data):
    file = io.BytesIO(data)
    file.name = "tmp.wav"
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
