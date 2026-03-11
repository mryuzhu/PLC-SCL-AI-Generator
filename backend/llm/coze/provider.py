from backend.llm.base import BaseProvider
from backend.llm.local.provider import LocalModelProvider


class CozeProvider(BaseProvider):
    def generate_code(self, prompt: str) -> str:
        # Placeholder fallback implementation; wire Coze API here.
        return LocalModelProvider().generate_code(prompt)
