import time

from llm import LanguageModel
from vocava import storage


class Translator:
    def __init__(self, model: LanguageModel):
        self._model = model

    def translate(self, text: str, from_language, to_language) -> str:
        prompt = f"Translate the TEXT from {from_language} to {to_language}\n" \
                 f"TEXT:\n\"{text}\""
        return self._model.generate(prompt)


class TranslationLanguageModel:
    def __init__(self, model: LanguageModel, translator: Translator,
                 native_language: str, target_language: str,
                 db: storage.VectorStore):
        self._model = model
        self._translator = translator
        self._native_language = native_language
        self._target_language = target_language
        self._last_translation = None
        self._db = db

    def _interaction_ids(self):
        message_id = int(time.time())
        return [
            f"{message_id}-user-{self._native_language}",
            f"{message_id}-user-{self._target_language}",
            f"{message_id}-bot-{self._target_language}",
            f"{message_id}-bot-{self._native_language}",
        ]

    def _interaction_metadata(self):
        return [
            {"language": self._native_language},
            {"language": self._target_language},
            {"language": self._target_language},
            {"language": self._native_language},
        ]

    def _save(self, docs):
        self._db.save(
            ids=self._interaction_ids(),
            documents=docs,
            metadata=self._interaction_metadata(),
        )

    def last_translation(self):
        prompt, translated_prompt, translated_response, response = self._last_translation
        return {
            'user': {
                self._native_language: prompt,
                self._target_language: translated_prompt,
            },
            'bot': {
                self._target_language: translated_response,
                self._native_language: response,
            },
        }

    def generate(self, prompt: str) -> str:
        translated_prompt = self._translator.translate(
            prompt,
            from_language=self._native_language,
            to_language=self._target_language,
        )
        translated_response = self._model.generate(translated_prompt)
        response = self._translator.translate(
            translated_response,
            from_language=self._target_language,
            to_language=self._native_language,
        )

        docs = [prompt, translated_prompt, translated_response, response]
        self._save(docs)
        self._last_translation = docs
        return translated_response
