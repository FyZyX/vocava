import os

import anthropic
import cohere
import streamlit as st
from streamlit_chat import message as chat_message

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
COHERE_API_KEY = st.secrets['cohere_api_key']

# Set your native and target languages
NATIVE_LANG = 'en'
TARGET_LANG = 'fr'


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


def main():
    st.set_page_config(
        page_title="Vocava - Demo",
        page_icon=":robot:"
    )

    st.header("Vocava")

    if 'history' not in st.session_state:
        st.session_state['history'] = []

    user_input = get_text()

    context = ""
    if user_input:
        # Translate user input to target language
        translated_input = translate(user_input, NATIVE_LANG, TARGET_LANG)

        current_inp = f"{anthropic.HUMAN_PROMPT} {translated_input}{anthropic.AI_PROMPT}"
        context += current_inp

        # Generate response in target language
        completion_translated = query(prompt=context)

        # Translate response back to native language
        completion = translate(completion_translated, TARGET_LANG, NATIVE_LANG)
        context += completion_translated

        # Get embeddings
        embeddings = embed([user_input, completion])
        embedding_user, embedding_bot = embeddings

        # Store in history
        st.session_state['history'].append({
            'user': {
                'text': user_input,
                'translated': translated_input,
                'embedding': embedding_user,
            },
            'bot': {
                'text': completion,
                'translated': completion_translated,
                'embedding': embedding_bot,
            }
        })

    if st.session_state['history']:
        for i in range(len(st.session_state['history']) - 1, -1, -1):
            message = st.session_state["history"][i]
            chat_message(message['bot']['text'], key=f"{i}")
            chat_message(message['user']['text'], is_user=True, key=f'{i}_user')


if __name__ == '__main__':
    main()
