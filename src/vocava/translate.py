from llm import LanguageModel


class Translator:
    def __init__(self, model: LanguageModel):
        self._model = model

    def translate(self, text: str, from_language, to_language) -> str:
        prompt = f"Translate the TEXT from {from_language} to {to_language}\n" \
                 f"TEXT:\n\"{text}\""
        return self._model.generate(prompt)
