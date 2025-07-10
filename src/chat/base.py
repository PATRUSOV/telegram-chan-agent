from src.ai.base import BaseLLM
from src.client.base import BaseClient
from typing import Dict

class Chat:
    llm: BaseLLM
    client: BaseClient
    opponent: Dict