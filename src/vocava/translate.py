import time

from llm import LanguageModel


class Translator:
    def __init__(self, model: LanguageModel):
        self._model = model

    def translate(self, text: str, from_language, to_language) -> str:
        prompt = f"Translate the TEXT from {from_language} to {to_language}\n" \
                 f"TEXT:\n\"{text}\""
        return self._model.generate(prompt)


class TranslatedInteraction:
    def __init__(self, documents, start_language, end_language):
        self._documents = documents
        self._start_language = start_language
        self._end_language = end_language

    def ids(self):
        message_id = int(time.time())
        return [
            f"{message_id}-user-{self._start_language}",
            f"{message_id}-user-{self._end_language}",
            f"{message_id}-bot-{self._end_language}",
            f"{message_id}-bot-{self._start_language}",
        ]

    def documents(self):
        return self._documents

    def metadata(self):
        return [
            {"language": self._start_language},
            {"language": self._end_language},
            {"language": self._end_language},
            {"language": self._start_language},
        ]

    def json(self):
        return {
            'user': {
                self._start_language: self._documents[0],
                self._end_language: self._documents[1],
            },
            'bot': {
                self._end_language: self._documents[2],
                self._start_language: self._documents[3],
            },
        }


class Chatterbox:
    def __init__(self, model: LanguageModel, translator: Translator,
                 native_language: str, target_language: str):
        self._model = model
        self._translator = translator
        self._native_language = native_language
        self._target_language = target_language
        self._last_translation = None

    def start_interaction(self, prompt: str) -> TranslatedInteraction:
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
        return TranslatedInteraction(docs, self._native_language, self._target_language)
