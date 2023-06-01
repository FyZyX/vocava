import json

import streamlit as st

from vocava.llm import anthropic
from vocava.llm.prompt import load_prompt
from vocava.translate import LANGUAGES

ANTHROPIC_API_KEY = st.secrets["anthropic_api_key"]


class JeopardyGame:
    def __init__(self, chatbot: anthropic.ClaudeChatBot):
        self._chatbot = chatbot

    def create_board(self, target_language, fluency):
        prompt = load_prompt(
            "games-jeopardy",
            target_language=target_language,
            fluency=fluency,
        )
        response = self._chatbot.generate(prompt, max_tokens=15_000)
        try:
            response = response.replace("```json", "").replace("```", "")
            start = response.find("{")
            payload = response[start:]
            data = json.loads(payload)
            return data
        except json.decoder.JSONDecodeError as e:
            st.error(e)
            st.write(response)


def main():
    st.title('Games')

    target_language = st.sidebar.selectbox(
        "Choose Language", options=LANGUAGES, index=12)
    fluency = st.sidebar.slider("Fluency", min_value=1, max_value=10, step=1)

    games = [
        "Jeopardy"
    ]
    game_name = st.selectbox("Select Game", options=games)

    if game_name == "Jeopardy":
        chatbot = anthropic.ClaudeChatBot(ANTHROPIC_API_KEY)
        game = JeopardyGame(chatbot)
        if st.button("New Game"):
            with st.spinner():
                board = game.create_board(
                    target_language=target_language,
                    fluency=fluency,
                )
                st.session_state["jeopardy-board"] = board
            st.json(board)
        board = st.session_state.get("jeopardy-board")
        if board:
            st.write(anthropic.count_tokens(str(board)))
            st.json(board)


if __name__ == "__main__":
    main()
