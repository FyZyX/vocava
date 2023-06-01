import anthropic


class Claude:
    def __init__(self, api_key: str):
        self._client = anthropic.Client(api_key=api_key)

    @staticmethod
    def wrap_prompt(text):
        return f"{anthropic.HUMAN_PROMPT} {text}{anthropic.AI_PROMPT}"

    def generate(self, prompt: str, max_tokens=200) -> str:
        return self._client.completion(
            prompt=self.wrap_prompt(prompt),
            stop_sequences=[anthropic.HUMAN_PROMPT],
            model="claude-v1-100k",
            max_tokens_to_sample=max_tokens,
        )["completion"]


class ClaudeChatBot(Claude):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self._history = ""

    def generate(self, prompt: str, max_tokens=200) -> str:
        self._history += self.wrap_prompt(prompt)
        response = self._client.completion(
            prompt=self._history,
            stop_sequences=[anthropic.HUMAN_PROMPT],
            model="claude-v1-100k",
            max_tokens_to_sample=max_tokens,
        )["completion"]
        self._history += f" {response}"
        return response
