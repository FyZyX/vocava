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
        response = self._chatbot.generate(prompt, max_tokens=5_000)
        try:
            response = response.replace("```json", "").replace("```", "")
            start = response.find("{")
            payload = response[start:]
            data = json.loads(payload)
            return data
        except json.decoder.JSONDecodeError as e:
            st.error(e)
            st.write(response)


def render_board(game_state):
    # Generate markdown table header
    markdown_table = "|   |" + " | ".join(
        [cat["name"] for cat in game_state["categories"]]) + " |\n"
    markdown_table += "|" + "----|" * (len(game_state["categories"]) + 1) + "\n"

    # Generate markdown table rows
    for i in range(5):  # 5 questions per category
        markdown_table += f"| {200 * (i + 1)} |"  # Start with the point value

        for cat in game_state["categories"]:
            # Check if the question has been answered
            is_answered = cat["questions"][i]["is_answered"]
            if is_answered:
                markdown_table += "   |"  # Empty cell for answered questions
            else:
                markdown_table += " ? |"  # Mark unanswered questions with a ?

        markdown_table += "\n"

    return markdown_table


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
            st.markdown(render_board(board))


if __name__ == "__main__":
    main()
