import json

from llm import LanguageModel
from llm.prompt import load_prompt

LANGUAGES = {
    "English": {"flag": "🇺🇸", "code": "en"},
    "German": {"flag": "🇩🇪", "code": "de"},
    "Polish": {"flag": "🇵🇱", "code": "pl"},
    "Spanish": {"flag": "🇪🇸", "code": "es"},
    "Italian": {"flag": "🇮🇹", "code": "it"},
    "French": {"flag": "🇫🇷", "code": "fr"},
    "Portuguese": {"flag": "🇵🇹", "code": "pt"},
    "Hindi": {"flag": "🇮🇳", "code": "hi"},
    "Arabic": {"flag": "🇸🇦", "code": "ar"},
    "Chinese": {"flag": "🇨🇳", "code": "zh"},
    "Greek": {"flag": "🇬🇷", "code": "el"},
    "Hebrew": {"flag": "🇮🇱", "code": "he"},
    "Japanese": {"flag": "🇯🇵", "code": "ja"},
    "Korean": {"flag": "🇰🇷", "code": "ko"},
    "Russian": {"flag": "🇷🇺", "code": "ru"},
    "Swedish": {"flag": "🇸🇪", "code": "sv"},
    "Tagalog": {"flag": "🇵🇭", "code": "tl"},
    "Vietnamese": {"flag": "🇻🇳", "code": "vi"},
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
