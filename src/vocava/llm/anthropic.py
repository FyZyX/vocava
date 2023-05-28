import anthropic


class Claude:
    def __init__(self, api_key: str):
        self._client = anthropic.Client(api_key=api_key)

    @staticmethod
    def _wrap_prompt(text):
        return anthropic.HUMAN_PROMPT + text + anthropic.AI_PROMPT

    def generate(self, prompt: str) -> str:
        return self._client.completion(
            prompt=self._wrap_prompt(prompt),
            stop_sequences=[anthropic.HUMAN_PROMPT],
            model="claude-v1.3-100k",
            max_tokens_to_sample=200,
        )["completion"]
