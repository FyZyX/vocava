import anthropic


class Claude:
    def __init__(self, api_key: str):
        self._client = anthropic.Client(api_key=api_key)

    @staticmethod
    def _wrap_prompt(text):
        return f"{anthropic.HUMAN_PROMPT} {text}{anthropic.AI_PROMPT}"

    def generate(self, prompt: str) -> str:
        return self._client.completion(
            prompt=self._wrap_prompt(prompt),
            stop_sequences=[anthropic.HUMAN_PROMPT],
            model="claude-v1-100k",
            max_tokens_to_sample=200,
        )["completion"]


class ClaudeChatBot(Claude):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self._history = ""

    def generate(self, prompt: str) -> str:
        self._history += self._wrap_prompt(prompt)
        response = self._client.completion(
            prompt=self._history,
            stop_sequences=[anthropic.HUMAN_PROMPT],
            model="claude-v1-100k",
            max_tokens_to_sample=200,
        )["completion"]
        self._history += f" {response}"
        return response
