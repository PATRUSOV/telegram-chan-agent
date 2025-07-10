from telethon import TelegramClient as _TelegramClient
from src.client.base import BaseClient
import asyncio
from dotenv import load_dotenv
import os
from telethon.tl.types import PeerUser
from telethon.errors import FloodWaitError
from telethon.tl.functions.messages import GetHistoryRequest
from typing import List, Dict
from telethon.tl.types import User
import logging

log = logging.getLogger(__name__)


load_dotenv()


API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")

def unwrap_getenv(key: str) -> None | str:
    value = os.getenv(key)
    if value is None:
        err_msg = f"Failed to get '{key}' from '.env'"
        log.info(err_msg)
        raise EnvironmentError(err_msg)
    return value

class TelegramClient(BaseClient):
    client = None
    client_data = {
        "API_ID": int(unwrap_getenv("API_ID")),
        "API_HASH": unwrap_getenv("API_HASH"),
        "PHONE_NUMBER": unwrap_getenv("PHONE_NUMBER"),
        "SESSION_NAME": "lhunter_session"
    }

    

    async def send_message(self, message: str, opponent: Dict) -> bool:
        """
        Send a message to a user by their Telegram ID.
        """
        if self.client is None:
            self.client = _TelegramClient(
            self.client_data["SESSION_NAME"],
            self.client_data["API_ID"],
            self.client_data["API_HASH"]
            )
            log.info("Launching telegram client authorization")
            await self.client.start(phone=self.client_data["PHONE_NUMBER"])
            log.info("Telegram client has successfully logged in")
        
        try:
            user_id = opponent["id"]
            await self.client.send_message(user_id, message)
            log.info(f"Message sent to user {user_id}")
            return True
        except Exception as e:
            log.error(f"Failed to send message to user {opponent.get('id')}: {e}")
            return False

    async def get_message(self, opponent: Dict) -> List[str]:
        """
        Вернуть тексты всех НЕпрочитанных входящих сообщений от одного пользователя.
        Предполагается, что self.client уже авторизован и запущен.
        """
        try:
            user_id = opponent["id"]

            # 1. Получаем диалог и узнаём read_inbox_max_id
            entity = await self.client.get_input_entity(user_id)
            dlg_info = await self.client(
                functions.messages.GetPeerDialogsRequest(peers=[entity])
            )
            read_max_id = dlg_info.dialogs[0].read_inbox_max_id or 0

            # 2. История сообщений «сразу после прочитанного»
            history = await self.client(GetHistoryRequest(
                peer=entity,
                limit=100,             # сколько сообщений максимум взять
                offset_id=0,
                max_id=0,
                min_id=read_max_id,    # ⬅️ всё, что новее read_max_id
                add_offset=0,
                hash=0
            ))

            # 3. Фильтр входящих + id > read_max_id
            unread_messages = [
                msg.message
                for msg in history.messages
                if isinstance(msg.from_id, type(entity))  # гарантирует, что это вообще сообщение
                and not msg.out                           # входящее
                and msg.id > read_max_id                  # действительно непрочитанное
            ]

            log.info(
                "Fetched %d unread messages from user %s",
                len(unread_messages),
                user_id,
            )
            return unread_messages

        # аккуратно обрабатываем FloodWait
        except FloodWaitError as e:
            wait = e.seconds + 1
            log.warning("FloodWait %ds on GetHistoryRequest, sleeping...", wait)
            await asyncio.sleep(wait)
            return await self.get_message(opponent)

        except Exception as exc:
            log.error("Failed to fetch messages from %s: %s", opponent.get("id"), exc)
            return []

    async def get_unread_user(self) -> List[int]:
        """
        Возвращает список ID пользователей с непрочитанными входящими сообщениями.
        """
        if self.client is None:
            self.client = _TelegramClient(
            self.client_data["SESSION_NAME"],
            self.client_data["API_ID"],
            self.client_data["API_HASH"]
            )
        try:
            dialogs = await self.client.get_dialogs()
            return [
                dialog.entity.id
                for dialog in dialogs
                if isinstance(dialog.entity, User) and dialog.unread_count > 0
            ]
        except Exception as e:
            log.error(f"Ошибка при получении ID пользователей с непрочитанными сообщениями: {e}")
            return []
        
        
    async def start(self):
        """Запуск клиента с авторизацией"""
        if self.client is None:
            self.client = _TelegramClient(
            self.client_data["SESSION_NAME"],
            self.client_data["API_ID"],
            self.client_data["API_HASH"]
            )
        log.info("Launching telegram client authorization")
        await self.client.start(phone=self.client_data["PHONE_NUMBER"])
        log.info("Telegram client has successfully logged in")
        async with self.client:
            while True:
                incoming_user = await self.get_unread_user()
                
                while not len(incoming_user):
                    await asyncio.sleep(2)
                    log.info(incoming_user)
                    incoming_user = await self.get_unread_user()

                for user in incoming_user:
                    msg = await self.get_message(opponent={"id": user})
                    msg = input(f"Enter message to {user}: " )
                    await self.send_message(msg, opponent={"id": user})
if __name__ == "__main__" :
    a = TelegramClient()
    asyncio.run(a.start())