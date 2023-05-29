from typing import Protocol


class LanguageModel(Protocol):
    def generate(self, prompt: str, max_tokens=250) -> str:
        pass
