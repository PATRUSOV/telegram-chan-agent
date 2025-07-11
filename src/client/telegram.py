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
from telethon import functions
import logging
from datetime import datetime
from typing import List, Dict, Optional
from telethon.tl.types import User


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
        try:
            user_id = opponent["id"]
            await self.client.send_message(user_id, message)
            log.info(f"Message sent to user {user_id}")
            return True
        except Exception as e:
            log.error(f"Failed to send message to user {opponent.get('id')}: {e}")
            return False

    async def get_message(self, opponent: Dict) -> List[str]:
        try:
            user_id = opponent["id"]
            entity = await self.client.get_input_entity(user_id)

            dlg_info = await self.client(
                functions.messages.GetPeerDialogsRequest(peers=[entity])
            )
            read_max_id = dlg_info.dialogs[0].read_inbox_max_id or 0

            # Вставляем offset_date как текущую дату
            history = await self.client(GetHistoryRequest(
                peer=entity,
                limit=100,
                offset_date=datetime.utcnow(),
                offset_id=0,
                max_id=0,
                min_id=read_max_id,
                add_offset=0,
                hash=0
            ))

            unread_messages = [
                msg.message
                for msg in history.messages
                if not msg.out and msg.id > read_max_id
            ]

            log.info(
                "Fetched %d unread messages from user %s",
                len(unread_messages),
                user_id,
            )
            return unread_messages

        except FloodWaitError as e:
            wait = e.seconds + 1
            log.warning("FloodWait %ds on GetHistoryRequest, sleeping...", wait)
            await asyncio.sleep(wait)
            return await self.get_message(opponent)

        except Exception as exc:
            log.error("Failed to fetch messages from %s: %s", opponent.get("id"), exc)
            return []

    async def mark_read(self, opponent: Dict) -> bool:
        """
        Пометить все входящие сообщения от пользователя как прочитанные.
        """
        try:
            user_id = opponent["id"]
            entity = await self.client.get_input_entity(user_id)

            await self.client(functions.messages.ReadHistoryRequest(
                peer=entity,
                max_id=0  # 0 означает "пометить всё"
            ))

            log.info("Marked all messages from user %s as read", user_id)
            return True

        except Exception as e:
            log.error("Failed to mark messages from %s as read: %s", opponent.get("id"), e)
            return False

        
    
    async def get_unread_user(self) -> List[Dict[str, Optional[str | int]]]:
        """
        Вернуть список пользователей, у которых есть непрочитанные входящие
        сообщения, в формате:
            [
                {"id": 123456789,
                "username": "@nickname" | None,
                "name": "Имя Фамилия" | None},
                ...
            ]
        """
        try:
            dialogs = await self.client.get_dialogs()
            unread_users: List[Dict[str, Optional[str | int]]] = []

            for dialog in dialogs:
                if isinstance(dialog.entity, User) and dialog.unread_count > 0:
                    user: User = dialog.entity
                    user_dict = {
                        "id": user.id,
                        "username": f"@{user.username}" if user.username else None,
                        "name": " ".join(filter(None, [user.first_name, user.last_name])) or None,
                    }
                    unread_users.append(user_dict)

            return unread_users

        except Exception as e:
            log.error("Ошибка при получении пользователей с непрочитанными сообщениями: %s", e)
            return []


    async def authorization(self) -> bool:
        if self.client is None:
            self.client = _TelegramClient(
                self.client_data["SESSION_NAME"],
                self.client_data["API_ID"],
                self.client_data["API_HASH"]
            )
        else:
            log.warning("Telegram client is already initialized, nothing to authorize")
        log.info("Launching telegram client authorization")
        try:
            await self.client.start(phone=self.client_data["PHONE_NUMBER"])
            log.info("Telegram client has successfully logged in")
            return True
        except Exception as e:
            log.error(f"Error during logging: {e}")
            return False

    async def deauthorization(self) -> bool:
        if self.client is None:
            log.warning("Telegram client is not initialized, nothing to deauthorize")
            return False

        log.info("Deauthorizing telegram client")
        try:
            await self.client.log_out()
            log.info("Telegram client has successfully logged out")
            return True
        except Exception as e:
            log.error(f"Error during logout: {e}")
            return False

    async def start(self):
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
                while not incoming_user:
                    await asyncio.sleep(2)
                    incoming_user = await self.get_unread_user()
                for user in incoming_user:
                    msg = await self.get_message(opponent={"id": user})
                    msg_text = input(f"Enter message to {user}: ")
                    await self.send_message(msg_text, opponent={"id": user})

if __name__ == "__main__":
    a = TelegramClient()
    asyncio.run(a.start())
