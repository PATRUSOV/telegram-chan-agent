from abc import ABC, abstractmethod


class BaseAI(ABC):
    @abstractmethod
    def set_bihavior(self): ...

    @abstractmethod
    def request(self): ...
