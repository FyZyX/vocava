import json

from llm import LanguageModel
from llm.prompt import load_prompt


class Translator:
    def __init__(self, model: LanguageModel):
        self._model = model

    def translate(self, text: str, from_language, to_language) -> dict[str, str]:
        prompt = load_prompt(
            "translate",
            text=text,
            from_language=from_language,
            to_language=to_language,
        )
        response = self._model.generate(prompt)
        data = json.loads(response)
        return data
