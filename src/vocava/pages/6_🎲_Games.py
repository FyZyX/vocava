import streamlit as st
import random


def main():
    st.title('Games')

    vocabulary = {
        "en": {"apple": "manzana", "dog": "perro", "house": "casa"},
        "fr": {"apple": "pomme", "dog": "chien", "house": "maison"},
        # Add more languages...
    }

    target_lang = st.sidebar.text_input("Target Language", "en")

    if target_lang in vocabulary:
        words = list(vocabulary[target_lang].keys())
        correct_word = random.choice(words)

        st.write(f"Translate the following word to {target_lang}: {correct_word}")

        user_answer = st.text_input("Your answer")

        if st.button("Check"):
            correct_answer = vocabulary[target_lang][correct_word]
            if user_answer == correct_answer:
                st.write("Correct!")
            else:
                st.write(
                    f"Sorry, that's not correct. The correct answer is {correct_answer}.")
    else:
        st.write("Sorry, we don't have games for this language yet.")


if __name__ == "__main__":
    main()
