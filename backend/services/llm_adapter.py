from backend.llm.base import BaseProvider
from backend.llm.coze.provider import CozeProvider
from backend.llm.local.provider import LocalModelProvider
from backend.llm.openai.provider import OpenAIProvider


class LLMAdapter:
    def __init__(self) -> None:
        self.providers: dict[str, BaseProvider] = {
            "coze": CozeProvider(),
            "openai": OpenAIProvider(),
            "local": LocalModelProvider(),
        }

    def generate_code(self, prompt: str, model: str) -> str:
        provider = self.providers.get(model, self.providers["local"])
        return provider.generate_code(prompt)
