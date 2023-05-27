import os

import anthropic
import streamlit as st
from streamlit_chat import message

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")


def query(prompt):
    client = anthropic.Client(api_key=ANTHROPIC_API_KEY)
    response = client.completion(
        prompt=f"{anthropic.HUMAN_PROMPT} {prompt}{anthropic.AI_PROMPT}",
        stop_sequences=[anthropic.HUMAN_PROMPT],
        model="claude-v1.3-100k",
        max_tokens_to_sample=100,
    )
    return response["completion"]


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
        st.session_state.past.append(user_input)
        context += current_inp

        completion = query(prompt=context)
        st.session_state.generated.append(completion)
        context += completion

    if st.session_state['generated']:
        for i in range(len(st.session_state['generated']) - 1, -1, -1):
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')


if __name__ == '__main__':
    main()
