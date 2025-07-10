from abc import ABC, abstractmethod


class BaseLLM(ABC):
    @abstractmethod
    def set_bihavior(self) -> None: ...

    @abstractmethod
    def request(self, msg: str) -> str: ...
