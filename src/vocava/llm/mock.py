class MockLanguageModel:
    def generate(self, prompt: str, max_tokens=250) -> str:
        return f"mock response for {prompt}"
