import os

import anthropic
import cohere
import streamlit as st
from streamlit_chat import message as chat_message

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
COHERE_API_KEY = st.secrets['cohere_api_key']


def query(prompt):
    client = anthropic.Client(api_key=ANTHROPIC_API_KEY)
    response = client.completion(
        prompt=prompt,
        stop_sequences=[anthropic.HUMAN_PROMPT],
        model="claude-v1.3-100k",
        max_tokens_to_sample=200,
    )
    return response["completion"]


def translate(text, src_lang, tgt_lang):
    client = anthropic.Client(api_key=ANTHROPIC_API_KEY)
    prompt = f"Translate the TEXT from {src_lang} to {tgt_lang}\n" \
             f"TEXT:\n\"{text}\""
    response = client.completion(
        prompt=prompt,
        stop_sequences=[anthropic.HUMAN_PROMPT],
        model="claude-v1.3-100k",
        max_tokens_to_sample=200,
    )
    return response["completion"]


def embed(docs: list[str]):
    cohere_client = cohere.Client(api_key=COHERE_API_KEY)
    return cohere_client.embed(texts=docs, model='embed-english')


def get_text():
    return st.text_input("You: ", "Hello, how are you?", key="input")


def chat_prompt(text):
    return f"{anthropic.HUMAN_PROMPT} {text}{anthropic.AI_PROMPT}"


def main():
    st.set_page_config(
        page_title="Vocava - Demo",
        page_icon=":robot:"
    )

    st.header("Vocava")

    col1, col2 = st.columns(2)
    native_lang = col1.text_input("Your native language: ", "en")
    target_lang = col2.text_input("Your target language: ", "fr")

    if 'history' not in st.session_state:
        st.session_state['history'] = []

    user_input = get_text()

    context = ""
    if user_input:
        translated_input = translate(user_input, native_lang, target_lang)
        context += chat_prompt(translated_input)

        completion = query(prompt=context)
        context += completion
        completion_translated = translate(completion, target_lang, native_lang)

        (
            embedding_user,
            embedding_user_translated,
            embedding_bot,
            embedding_bot_translated,
        ) = embed([
            user_input,
            translated_input,
            completion,
            completion_translated,
        ])

        st.session_state['history'].append({
            'user': {
                native_lang: user_input,
                target_lang: translated_input,
                'embedding': embedding_user,
            },
            'bot': {
                native_lang: completion,
                target_lang: completion_translated,
                'embedding': embedding_bot,
            }
        })

    if st.session_state['history']:
        view_target = st.checkbox('View in target language')
        for i in range(len(st.session_state['history']) - 1, -1, -1):
            message = st.session_state["history"][i]
            language = target_lang if view_target else native_lang
            chat_message(message['bot'][language], key=f"{i}")
            chat_message(message['user'][language], is_user=True, key=f'{i}_user')


if __name__ == '__main__':
    main()
