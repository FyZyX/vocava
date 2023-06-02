import typing

import llm
import llm.prompt

JSON = None | bool | int | float | str | dict[str, "JSON"] | list["JSON"]

Language: typing.TypeAlias = str
LANGUAGES: dict[Language, dict[str, str]] = {
    "🇺🇸 English": {"name": "English", "flag": "🇺🇸", "code": "en"},
    "🇩🇪 German": {"name": "German", "flag": "🇩🇪", "code": "de"},
    "🇵🇱 Polish": {"name": "Polish", "flag": "🇵🇱", "code": "pl"},
    "🇪🇸 Spanish": {"name": "Spanish", "flag": "🇪🇸", "code": "es"},
    "🇮🇹 Italian": {"name": "Italian", "flag": "🇮🇹", "code": "it"},
    "🇫🇷 French": {"name": "French", "flag": "🇫🇷", "code": "fr"},
    "🇵🇹 Portuguese": {"name": "Portuguese", "flag": "🇵🇹", "code": "pt"},
    "🇮🇳 Hindi": {"name": "Hindi", "flag": "🇮🇳", "code": "hi"},
    "🇸🇦 Arabic": {"name": "Arabic", "flag": "🇸🇦", "code": "ar"},
    "🇨🇳 Chinese": {"name": "Chinese", "flag": "🇨🇳", "code": "zh"},
    "🇬🇷 Greek": {"name": "Greek", "flag": "🇬🇷", "code": "el"},
    "🇮🇱 Hebrew": {"name": "Hebrew", "flag": "🇮🇱", "code": "he"},
    "🇯🇵 Japanese": {"name": "Japanese", "flag": "🇯🇵", "code": "ja"},
    "🇰🇷 Korean": {"name": "Korean", "flag": "🇰🇷", "code": "ko"},
    "🇷🇺 Russian": {"name": "Russian", "flag": "🇷🇺", "code": "ru"},
    "🇸🇪 Swedish": {"name": "Swedish", "flag": "🇸🇪", "code": "sv"},
    "🇵🇭 Tagalog": {"name": "Tagalog", "flag": "🇵🇭", "code": "tl"},
    "🇻🇳 Vietnamese": {"name": "Vietnamese", "flag": "🇻🇳", "code": "vi"},
}


class Service:
    def __init__(self, name: str, model: llm.LanguageModel,
                 native_language: Language, target_language: Language,
                 native_mode: bool = False, max_tokens: int = 250):
        self._model = model
        self._name = name
        self._native_language = native_language
        self._target_language = target_language
        self._native_mode = native_mode
        self._languages: dict[Language, dict[str, str]] = LANGUAGES

    def get_language_name(self, language: Language):
        return self._languages[language]["name"]

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
        response = self._model.generate(prompt, max_tokens=max_tokens)
        return llm.prompt.extract_json(response)
