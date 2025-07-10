import os
import dotenv
import logging

from mistralai import Mistral
from typing import override

from src.ai.base import BaseAI

dotenv.load_dotenv()
logger = logging.getLogger(__name__)


class MistralAI(BaseAI):
    def __init__(self):
        self._API = os.environ.get("MISTRAL_API_KEY")
        if self._API is None:
            error_msg = "Переменная окружения MISTRAL_API_KEY не существует."
            logger.fatal(error_msg)
            raise RuntimeError(error_msg)
        self._model = "mistral-medium-2505"
        self._client = Mistral(self._API)

    @override
    def request(self, msg: str) -> str:
        # self._client.chat.complete()
        ...
