import typing

from vocava import llm
from vocava.llm import anthropic, mock

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
USER_VOCABULARY = {
    "Japanese": {
        "はじめまして": ["How do you do?", "Nice to meet you"],
        "うれしい": ["happy", "glad", "joyful"],
        "つくづく": ["really", "indeed"],
        "ストーブ": ["stove"],
        "さすがに": ["as expected", "sure enough"],
        "ありゃありゃ": ["my my", "dear me"],
        "あざとい": ["showy", "flashy", "gaudy"],
        "ohayou gozaimasu": ["good morning", "hello"],
        "konnichiwa": ["good day", "hello"],
        "oyasumi nasai": ["good night"],
        "sumimasen": ["excuse me"],
        "arigatou gozaimasu": ["thank you"],
        "nani o shimasu ka": ["what are you doing?"],
        "sore wa totemo oishii desu": ["that is very tasty"],
    }
}
USER_PHRASES = {
    "Japanese": {
    }
}


class User:
    def __init__(self, native_language: Language, target_language: Language,
                 fluency: int):
        self._native_language = native_language
        self._target_language = target_language
        self._fluency = fluency
        self._languages: dict[Language, dict[str, str]] = LANGUAGES
        self._vocabulary = USER_VOCABULARY
        self._phrases = USER_PHRASES

    def _get_language_name(self, language: Language):
        return self._languages[language]["name"]

    def native_language_name(self) -> str:
        return self._get_language_name(self._native_language)

    def target_language_name(self) -> str:
        return self._get_language_name(self._target_language)

    def _get_language_code(self, language: Language):
        return self._languages[language]["code"]

    def target_language_code(self) -> str:
        return self._get_language_code(self._target_language)

    def known_vocabulary(self):
        return self._vocabulary.get(self.target_language_name())

    def known_phrases(self):
        return self._phrases.get(self.target_language_name())

    def fluency(self):
        return self._fluency


class Tutor:
    def __init__(self, model: llm.LanguageModel):
        self._model = model

    def ask(self, prompt: str, max_tokens: int = 250):
        return self._model.generate(prompt, max_tokens=max_tokens)


def get_tutor(model, key=None) -> Tutor:
    if model == "Claude":
        model = anthropic.Claude(api_key=key)
    else:
        model = mock.MockLanguageModel()
    tutor = Tutor(model)
    return tutor
