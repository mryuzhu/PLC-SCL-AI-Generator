from backend.llm.base import BaseProvider
from backend.llm.local.provider import LocalModelProvider


class OpenAIProvider(BaseProvider):
    def generate_code(self, prompt: str) -> str:
        # Placeholder fallback implementation; wire OpenAI-compatible endpoint here.
        return LocalModelProvider().generate_code(prompt)
