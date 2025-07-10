from telethon import TelegramClient as _TelegramClient
from base import BaseClient
import asyncio
from dotenv import load_dotenv
import os
from telethon import TelegramClient as _TelegramClient
from telethon.tl.types import PeerUser
from telethon.errors import FloodWaitError
from telethon.tl.functions.messages import GetHistoryRequest
import logging


load_dotenv()



API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")


class TelegramClient(BaseClient):
    client_data = {
        "API_ID": int(os.getenv("API_ID")),
        "API_HASH": os.getenv("API_HASH"),
        "PHONE_NUMBER": os.getenv("PHONE_NUMBER"),
        "SESSION_NAME": "lhunter_session"
    }

    client = _TelegramClient(
        client_data["SESSION_NAME"],
        client_data["API_ID"],
        client_data["API_HASH"]
    )

    async def start(self):
        """Запуск клиента с авторизацией"""
        await self.client.start(phone=self.client_data["PHONE_NUMBER"])
        loggin.info

    async def send_message(self, opponent, message: str = "Привет от клиента!") -> bool:
        """Отправка сообщения одному пользователю"""
        try:
            await self.client.send_message(opponent, message)
            print(f"[✓] Сообщение отправлено: {opponent}")
            return True
        except FloodWaitError as e:
            print(f"[!] FloodWait: подожди {e.seconds} секунд")
            return False
        except Exception as e:
            print(f"[!] Ошибка при отправке: {e}")
            return False

    async def get_message(self, opponent_list: list) -> str:
        """
        Получение последнего сообщения от списка пользователей.
        Возвращает текст первого найденного сообщения.
        """
        for opponent in opponent_list:
            try:
                history = await self.client(GetHistoryRequest(
                    peer=opponent,
                    limit=1,
                    offset_date=None,
                    offset_id=0,
                    max_id=0,
                    min_id=0,
                    add_offset=0,
                    hash=0
                ))
                if history.messages:
                    msg = history.messages[0].message
                    print(f"[✓] Последнее сообщение от {opponent}: {msg}")
                    return msg
            except Exception as e:
                print(f"[!] Ошибка при получении сообщения от {opponent}: {e}")
        return ""