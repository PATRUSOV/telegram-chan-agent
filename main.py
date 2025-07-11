"""from src.llm.mistral import MistralClient, ChatSession
from dotenv import load_dotenv
import os


mistral = MistralClient(
    api_key=os.environ.get("MISTRAL_API_KEY"), model="mistral-medium-2505"
)
session = ChatSession(mistral)

while True:
    print(session.send(input()))
"""

import asyncio
from src.client import TelegramClient  # Убедись, что TelegramClient импортируется правильно
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

async def main():
    opponent = {
        "id": 743773746  # ID пользователя, с которым идёт чат
    }

    client = TelegramClient()
    await client.authorization()
    try:
        while True:
            unread_users = await client.get_unread_user()
            if opponent['id'] in unread_users:
                msg_recv = await client.get_message(opponent=opponent)
                log.info(f"Successfully marked up all messages from {opponent['id']}") if \
                    await client.mark_read(opponent=opponent) else \
                        log.error(f"Failed to marked up messages from {opponent['id']}")
                print(f"Message from {opponent['id']}:\n{msg_recv}")
                msg_send = input(f"Message to {opponent['id']}: ")
                await client.send_message(message=msg_send, opponent=opponent)
            else:
                log.info(f"No unread messages from {opponent['id']}")
                await asyncio.sleep(2)
    except KeyboardInterrupt:
        log.info("Stopped by user")
    except Exception as e:
        log.error(f"Unexpected error: {e}")
    finally:
        ...
        # await client.deauthorization()

asyncio.run(main())
