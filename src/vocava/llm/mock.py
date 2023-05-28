class MockLanguageModel:
    def generate(self, prompt: str) -> str:
        return f"mock response for {prompt}"
