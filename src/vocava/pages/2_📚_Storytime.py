import streamlit as st

from vocava.llm import LanguageModel, anthropic, mock

ANTHROPIC_API_KEY = st.secrets["anthropic_api_key"]


class StoryGenerator:
    def __init__(self, model: LanguageModel):
        self._model = model

    def generate_story(self, prompt: str) -> str:
        # Extend this method to generate a short story based on the prompt
        return self._model.generate(prompt)


class ComprehensionTester:
    def __init__(self, model: LanguageModel):
        self._model = model

    def generate_questions(self, text: str) -> str:
        # Extend this method to generate comprehension questions based on the text
        return self._model.generate(
            f"Generate comprehension questions for the following text:\n{text}")


def storyteller_page():
    st.title('Storyteller')

    user_prompt = st.text_input("Enter a prompt for a story")
    if st.button("Generate Story"):
        model = anthropic.Claude(ANTHROPIC_API_KEY)
        model = mock.MockLanguageModel()
        story_gen = StoryGenerator(model)
        generated_story = story_gen.generate_story(user_prompt)
        st.text_area("Generated Story", generated_story)

        tester = ComprehensionTester(model)
        comprehension_questions = tester.generate_questions(generated_story)
        st.text_area("Comprehension Questions", comprehension_questions)


def main():
    storyteller_page()


if __name__ == "__main__":
    main()
