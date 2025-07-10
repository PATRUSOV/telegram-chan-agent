import asyncio
from .ai import request
from .client.telegram import telegram_client, PHONE_NUMBER
# from .chat import Chat


async def main():
    await telegram_client.start(phone=PHONE_NUMBER)

    username = 'targetusername'  # Без @
    message = 'Привет! Это автоматическое сообщение.'
    await telegram_client.send_message(username, message)

    ("Сообщение отправлено")

with telegram_client:
    telegram_client.loop.run_until_complete(main())