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
        prompt=f"{anthropic.HUMAN_PROMPT} {prompt}{anthropic.AI_PROMPT}",
        stop_sequences=[anthropic.HUMAN_PROMPT],
        model="claude-v1.3-100k",
        max_tokens_to_sample=100,
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

    if 'generated' not in st.session_state:
        st.session_state['generated'] = []

    if 'past' not in st.session_state:
        st.session_state['past'] = []

    user_input = get_text()

    context = ""
    if user_input:
        current_inp = f"{anthropic.HUMAN_PROMPT} {user_input}{anthropic.AI_PROMPT}"
        context += current_inp

        completion = query(prompt=context)
        context += completion

        embedding_user, embedding_bot = embed([user_input, completion])

        st.session_state['past'].append((user_input, embedding_user))
        st.session_state['generated'].append((completion, embedding_bot))

    if st.session_state['generated']:
        for i in range(len(st.session_state['generated']) - 1, -1, -1):
            chat_message(st.session_state["generated"][i][0], key=str(i))
            chat_message(st.session_state['past'][i][0], is_user=True, key=f'{i}_user')


if __name__ == '__main__':
    main()
