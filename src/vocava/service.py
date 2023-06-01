import llm
import llm.prompt

JSON = None | bool | int | float | str | dict[str, "JSON"] | list["JSON"]


class Service:
    def __init__(self, name: str, model: llm.LanguageModel):
        self._model = model
        self._name = name

    def run(self, native_language: str, target_language: str, **kwargs) -> JSON:
        prompt = llm.prompt.load_prompt(
            self._name,
            native_language=native_language,
            target_language=target_language,
            **kwargs
        )
        response = self._model.generate(prompt)
        return llm.prompt.extract_json(response)
