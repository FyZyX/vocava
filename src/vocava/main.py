import requests
import streamlit as st
from streamlit_chat import message


def query(payload):
    API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
    headers = {"Authorization": st.secrets['api_key']}

    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


def get_text():
    return st.text_input("You: ", "Hello, how are you?", key="input")


def main():
    st.set_page_config(
        page_title="Streamlit Chat - Demo",
        page_icon=":robot:"
    )

    st.header("Vocava - Demo")

    if 'generated' not in st.session_state:
        st.session_state['generated'] = []

    if 'past' not in st.session_state:
        st.session_state['past'] = []

    user_input = get_text()

    if user_input:
        output = query({
            "inputs": {
                "past_user_inputs": st.session_state.past,
                "generated_responses": st.session_state.generated,
                "text": user_input,
            }, "parameters": {"repetition_penalty": 1.33},
        })

        st.session_state.past.append(user_input)
        st.session_state.generated.append(output["generated_text"])

    if st.session_state['generated']:

        for i in range(len(st.session_state['generated']) - 1, -1, -1):
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')


if __name__ == '__main__':
    main()
