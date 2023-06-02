import llm
import llm.prompt
from vocava.entity import Language

JSON = None | bool | int | float | str | dict[str, "JSON"] | list["JSON"]


class Service:
    def __init__(self, name: str, model: llm.LanguageModel,
                 native_language: Language, target_language: Language,
                 native_mode: bool = False, max_tokens: int = 250):
        self._model = model
        self._name = name
        self._native_language = native_language
        self._target_language = target_language
        self._native_mode = native_mode
        self._max_tokens = max_tokens

    def toggle_native_mode(self):
        self._native_mode = not self._native_mode

    def is_in_native_mode(self) -> bool:
        return self._native_mode

    def current_language(self):
        return self.get_language_name(
            self._native_language if self._native_mode else self._target_language)

    def run(self, **kwargs) -> JSON:
        prompt = llm.prompt.load_prompt(
            self._name,
            native_language=self.get_language_name(self._native_language),
            target_language=self.get_language_name(self._target_language),
            **kwargs
        )
        response = self._model.generate(prompt, max_tokens=self._max_tokens)
        return llm.prompt.extract_json(response)
