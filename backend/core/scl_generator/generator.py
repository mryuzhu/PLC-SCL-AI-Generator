from backend.core.prompt_engine.engine import PromptContext, PromptEngine
from backend.services.llm_adapter import LLMAdapter


class SCLGenerator:
    def __init__(self, prompt_engine: PromptEngine | None = None, llm_adapter: LLMAdapter | None = None) -> None:
        self.prompt_engine = prompt_engine or PromptEngine()
        self.llm_adapter = llm_adapter or LLMAdapter()

    def generate(self, requirement: str, mode: str = "balanced", model: str = "local", template: str | None = None) -> str:
        prompt = self.prompt_engine.build(PromptContext(requirement=requirement, mode=mode, template=template))
        return self.llm_adapter.generate_code(prompt=prompt, model=model)
