import typing

import vocava.llm.anthropic
import vocava.llm.mock

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


class User:
    def __init__(self, native_language: Language, target_language: Language,
                 fluency: int):
        self._native_language = native_language
        self._target_language = target_language
        self._fluency = fluency
        self._languages: dict[Language, dict[str, str]] = LANGUAGES

    def _get_language_name(self, language: Language):
        return self._languages[language]["name"]

    def native_language_name(self) -> str:
        return self._get_language_name(self._native_language)

    def target_language_name(self) -> str:
        return self._get_language_name(self._native_language)

    def fluency(self):
        return self._fluency


class Tutor:
    def __init__(self, model: vocava.llm.LanguageModel):
        self._model = model

    def ask(self, prompt: str, max_tokens: int = 250):
        self._model.generate(prompt, max_tokens=max_tokens)


def get_tutor(model, key=None) -> Tutor:
    if model == "Claude":
        model = vocava.llm.anthropic.Claude(api_key=key)
    else:
        model = vocava.llm.mock.MockLanguageModel()
    tutor = Tutor(model)
    return tutor
