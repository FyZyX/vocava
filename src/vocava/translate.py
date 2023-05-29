import json

from llm import LanguageModel
from llm.prompt import load_prompt

LANGUAGES = {
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
