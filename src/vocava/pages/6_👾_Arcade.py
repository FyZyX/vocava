import json

import openai
import streamlit as st

from vocava.llm import anthropic
from vocava.llm.prompt import load_prompt
from vocava.translate import LANGUAGES

ANTHROPIC_API_KEY = st.secrets["anthropic_api_key"]


class Arcade:
    def __init__(self, chatbot: anthropic.Claude):
        self._chatbot = chatbot

    def create_jeopardy_game(self, native_language, target_language, fluency):
        prompt = load_prompt(
            "arcade-jeopardy",
            native_language=native_language,
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

    def new_pictionary_game(self, native_language, target_language, fluency):
        prompt = load_prompt(
            "arcade-pictionary",
            native_language=native_language,
            target_language=target_language,
            fluency=fluency,
        )
        response = self._chatbot.generate(prompt, max_tokens=200)
        try:
            response = response.replace("```json", "").replace("```", "")
            start = response.find("{")
            payload = response[start:]
            data = json.loads(payload)
        except json.decoder.JSONDecodeError as e:
            st.error(e)
            st.write(response)
        else:
            response = openai.Image.create(
                prompt=data["prompt"],
                n=1,
                size="512x512",
            )
            image_url = response['data'][0]['url']
            data.update(url=image_url)
            return data


def render_board(game_state):
    # Generate markdown table header
    markdown_table = "|   | " + " | ".join(
        [cat["name"] for cat in game_state["categories"]]) + " |\n"
    markdown_table += "|" + "---|" * (len(game_state["categories"]) + 1) + "\n"

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


def play_jeopardy(native_language_name, target_language_name, fluency):
    chatbot = anthropic.ClaudeChatBot(ANTHROPIC_API_KEY)
    game = Arcade(chatbot)
    if st.button("New Game"):
        with st.spinner():
            board = game.create_jeopardy_game(
                native_language=native_language_name,
                target_language=target_language_name,
                fluency=fluency,
            )
            st.session_state["jeopardy-board"] = board
    board = st.session_state.get("jeopardy-board")
    if not board:
        return
    st.markdown(render_board(board))
    st.divider()
    cols = st.columns(2)
    with cols[0]:
        categories = [category["name"] for category in board["categories"]]
        category = st.selectbox("Select Topic", options=categories)
    with cols[1]:
        points = st.number_input(
            "Select Points", min_value=200, max_value=1000, step=200)

    if st.button("Go"):
        index = categories.index(category)
        question = board["categories"][index]["questions"][points // 200 - 1]
        st.session_state["current_question"] = question
    if st.session_state.get("current_question"):
        question = st.session_state["current_question"]
        if question.get("is_answered"):
            st.error("You've already answered this question!")
            return
        st.write(question["text"])
        answer = st.text_input("Answer")
        if not answer:
            return
        question["is_answered"] = True
        if answer != question["answer"]:
            st.error("Unfortunately, that's not correct.")
        else:
            st.success("Good job!")
        del st.session_state["current_question"]


def play_pictionary(native_language, target_language, fluency):
    model = anthropic.Claude(ANTHROPIC_API_KEY)
    game = Arcade(model)
    if st.button("New Game"):
        with st.spinner():
            data = game.new_pictionary_game(
                native_language=native_language,
                target_language=target_language,
                fluency=fluency,
            )
            st.session_state["pitctionary"] = data
    data = st.session_state.get("pitctionary")
    if not data:
        return
    word = data["word"]
    translation = data["translation"]
    url = data["url"]
    st.image(url)
    guess = st.text_input("Guess").lower()
    if st.button("Guess"):
        if guess == data["word"].lower():
            st.success("Good job!")
        else:
            st.info(data["prompt"])
            st.error(f"Sorry, the word was actually {word} ({translation})")


def main():
    st.title('Games')

    native_language = st.sidebar.selectbox("Choose Language", options=LANGUAGES)
    target_language = st.sidebar.selectbox(
        "Choose Language", options=LANGUAGES, index=12)
    native_language_name = LANGUAGES[native_language]["name"]
    target_language_name = LANGUAGES[target_language]["name"]
    fluency = st.sidebar.slider("Fluency", min_value=1, max_value=10, step=1)

    games = [
        "Jeopardy",
        "Pictionary",
    ]
    game_name = st.selectbox("Select Game", options=games)

    if game_name == "Jeopardy":
        play_jeopardy(native_language_name, target_language_name, fluency)
    elif game_name == "Pictionary":
        play_pictionary(native_language, target_language_name, fluency)


if __name__ == "__main__":
    main()
