from abc import ABC, abstractmethod


class BaseProvider(ABC):
    @abstractmethod
    def generate_code(self, prompt: str) -> str:
        raise NotImplementedError
