import streamlit as st

from vocava.llm import anthropic
from vocava.llm.prompt import load_prompt
from vocava.translate import LANGUAGES

ANTHROPIC_API_KEY = st.secrets["anthropic_api_key"]


class JeopardyGame:
    def __init__(self, chatbot: anthropic.ClaudeChatBot):
        self._chatbot = chatbot

    def start_game(self, target_language, fluency):
        prompt = load_prompt(
            "games-jeopardy",
            target_language=target_language,
            fluency=fluency,
        )
        response = self._chatbot.generate(prompt, max_tokens=500)
        return prompt, response

    def select_next_question(self, topic, points, history):
        prompt = f"I'd like {topic} for {points} please"
        history.append(prompt)
        chat_history = "".join([self._chatbot.wrap_prompt(x) for x in history])
        response = self._chatbot.generate(chat_history, max_tokens=500)
        history.append(response)
        return prompt, response

    def submit_answer(self, answer, history):
        prompt = f"My answer is {answer}."
        history.append(prompt)
        chat_history = "".join([self._chatbot.wrap_prompt(x) for x in history])
        response = self._chatbot.generate(chat_history, max_tokens=500)
        history.append(response)
        return prompt, response


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
                prompt, board = game.start_game(
                    target_language=target_language,
                    fluency=fluency,
                )
            st.session_state["jeopardy"] = [prompt, board]
            st.session_state["jeopardy-board"] = board
            st.session_state["jeopardy-in-game"] = True
        if "jeopardy-in-game" in st.session_state:
            board = st.session_state["jeopardy-board"]
            st.session_state["jeopardy-board"] = board
            st.markdown(board)
        else:
            return

        st.write("Pick a topic and point value to start playing!")
        cols = st.columns(2)
        with cols[0]:
            topic = st.text_input("Topic")
        with cols[1]:
            points = st.number_input("Points", min_value=200, max_value=1000, step=200)

        history = st.session_state["jeopardy"]
        if st.button("Get Next Question"):
            with st.spinner():
                prompt, question = game.select_next_question(
                    topic, points, history=history)
            st.markdown(question)
            st.session_state["jeopardy-question"] = True
        if st.session_state.get("jeopardy-question", False):
            answer = st.text_input("Your Answer")
            if answer:
                with st.spinner():
                    prompt, board = game.submit_answer(answer, history=history)
                st.session_state["jeopardy-board"] = board
                st.markdown(board)
                if st.button("Continue"):
                    st.session_state["jeopardy-question"] = False


if __name__ == "__main__":
    main()
