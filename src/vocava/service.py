import llm.prompt
from vocava import entity

JSON = None | bool | int | float | str | dict[str, "JSON"] | list["JSON"]


class Service:
    def __init__(self, name: str, user: entity.User, tutor: entity.Tutor,
                 native_mode: bool = False, max_tokens: int = 250,
                 extract_json: bool = True):
        self._tutor = tutor
        self._name = name
        self._user = user
        self._native_mode = native_mode
        self._max_tokens = max_tokens
        self._extract_json = extract_json

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
        response = self._tutor.ask(prompt, max_tokens=self._max_tokens)
        if self._extract_json:
            return llm.prompt.extract_json(response)
        else:
            return response
