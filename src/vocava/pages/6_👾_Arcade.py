import openai
import streamlit as st

from vocava import entity, service

ANTHROPIC_API_KEY = st.secrets["anthropic_api_key"]


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


def play_jeopardy(user, tutor):
    game = service.Service(
        "arcade-jeopardy",
        user=user,
        tutor=tutor,
        max_tokens=200,
    )
    if st.button("New Game"):
        with st.spinner():
            data = game.run(fluency=user.fluency())
        st.session_state["jeopardy.board"] = data

    board = st.session_state.get("jeopardy.board")
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
        st.session_state["jeopardy.question"] = question

    if st.session_state.get("jeopardy.question"):
        question = st.session_state["jeopardy.question"]
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
        del st.session_state["jeopardy.question"]


def play_pictionary(user, tutor):
    game = service.Service(
        "arcade-pitctionary",
        user=user,
        tutor=tutor,
        max_tokens=200,
    )
    if st.button("New Game"):
        with st.spinner():
            data = game.run(fluency=user.fluency())
            response = openai.Image.create(
                prompt=data["prompt"],
                n=1,
                size="256x256",
            )
        image_url = response['data'][0]['url']
        data.update(url=image_url)
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


def play_mad_libs(user, tutor):
    game = service.Service(
        "arcade-mad-libs-create",
        user=user,
        tutor=tutor,
        max_tokens=300,
    )
    if st.button("New Game"):
        with st.spinner():
            data = game.run(fluency=user.fluency())
        st.session_state["mad-libs"] = data

    data = st.session_state.get("mad-libs")
    if not data:
        return
    text = data["text"]
    blanks = data["blanks"]
    answers = []
    cols = st.columns(3)
    for i, blank in enumerate(blanks):
        with cols[i % 3]:
            answers.append(st.text_input(blank, key=i))
    if st.button("Submit"):
        grader = service.Service(
            "arcade-mad-libs-grade",
            user=user,
            tutor=tutor,
            max_tokens=650,
        )
        with st.spinner():
            data = grader.run(
                fluency=user.fluency(),
                original=text,
                words=answers,
            )
        st.markdown(data["output"])
        st.info(data["translation"])
        st.metric("Total Points", data["points"])


def play_odd_one_out(user, tutor):
    view_native = st.checkbox("Native View")
    game = service.Service(
        "arcade-odd-one-out",
        user=user,
        tutor=tutor,
        native_mode=view_native,
        max_tokens=650,
    )
    if st.button("New Game"):
        with st.spinner():
            data = game.run(fluency=user.fluency())
        st.session_state["odd-one-out"] = data

    data = st.session_state.get("odd-one-out")
    language = game.current_language()
    if not data or language not in data:
        return
    words = data[language]["words"]
    theme = data[language]["theme"]
    answer = data[language]["answer"]
    cols = st.columns(3)
    for i, word in enumerate(words):
        with cols[i % 3]:
            st.markdown(word)
    guess = st.selectbox("Pick the :green[Odd One Out]!", options=words)
    if st.button("Guess") and guess:
        if guess.strip().lower() == answer.strip().lower():
            st.success("Good job!")
            st.info(theme)
        else:
            st.error("Sorry, that's not right.")


def main():
    st.title('Arcade')

    languages = list(entity.LANGUAGES)
    default_native_lang = st.session_state.get("user.native_lang", languages[0])
    default_target_lang = st.session_state.get("user.target_lang", languages[4])
    default_fluency = st.session_state.get("user.fluency", 3)
    native_language = st.sidebar.selectbox(
        "Native Language", options=entity.LANGUAGES,
        index=languages.index(default_native_lang),
    )
    target_language = st.sidebar.selectbox(
        "Choose Language", options=entity.LANGUAGES,
        index=languages.index(default_target_lang),
    )
    fluency = st.sidebar.slider("Fluency", min_value=1, max_value=10, step=1,
                                value=default_fluency)
    user = entity.User(
        native_language=native_language,
        target_language=target_language,
        fluency=fluency,
    )
    st.session_state["user.native_lang"] = native_language
    st.session_state["user.target_lang"] = target_language
    st.session_state["user.fluency"] = fluency
    tutor = entity.get_tutor("Claude", key=ANTHROPIC_API_KEY)

    games = [
        "Pictionary",
        "Odd One Out",
        "Mad Libs",
        "Jeopardy",
    ]
    game_name = st.selectbox("Select Game", options=games)

    if game_name == "Jeopardy":
        play_jeopardy(user, tutor)
    elif game_name == "Pictionary":
        play_pictionary(user, tutor)
    elif game_name == "Mad Libs":
        play_mad_libs(user, tutor)
    elif game_name == "Odd One Out":
        play_odd_one_out(user, tutor)


if __name__ == "__main__":
    main()
