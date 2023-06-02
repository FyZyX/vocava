import llm
import llm.prompt
from vocava import entity

JSON = None | bool | int | float | str | dict[str, "JSON"] | list["JSON"]


class Service:
    def __init__(self, name: str, user: entity.User, model: llm.LanguageModel,
                 native_mode: bool = False, max_tokens: int = 250):
        self._model = model
        self._name = name
        self._user = user
        self._native_mode = native_mode
        self._max_tokens = max_tokens

    def toggle_native_mode(self):
        self._native_mode = not self._native_mode

    def is_in_native_mode(self) -> bool:
        return self._native_mode

    def current_language(self) -> str:
        return (self._user.native_language_name()
                if self._native_mode else
                self._user.target_language_name())

    def run(self, **kwargs) -> JSON:
        prompt = llm.prompt.load_prompt(
            self._name,
            native_language=self._user.native_language_name(),
            target_language=self._user.target_language_name(),
            **kwargs
        )
        response = self._model.generate(prompt, max_tokens=self._max_tokens)
        return llm.prompt.extract_json(response)
