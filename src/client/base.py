from abc import ABC, abstractmethod
from typing import Dict

class BaseClient(ABC):
    client_data: Dict
    
    @abstractmethod
    async def get_message(self, opponent: Dict) -> str: ...
    
    @abstractmethod
    async def send_message(self, opponent: Dict) -> bool: ...
    