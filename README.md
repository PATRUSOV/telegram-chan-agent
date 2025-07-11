# English:
## Telegram Chan Agent 
is an *AI agent* for telegram (and not only) account. 
## The agent supports (telegram): 
- the authorization of account telegrams
- receiving the account IDs of opponents from whom the agent has unread messages 
- Receiving unread messages by the opponent's ID 
- Mark as read for all messages during the opponent's ID 
- Sending messages by the opponent's account ID 
- Text processing using the LLM API
- Support for asynchronous chat with an opponent

## Repository:
```
telegram-chan-agent/ 
├── main.py                 -   *Entry point to the program* 
├── .env                    -   *Environment with your API keys*
├── README.md               -   *Read me file (this file)* 
├── requirements.txt        -   *Python program dependencies* 
└── src                     -   *The source code directory* 
    ├── __init__.py         -   *Initial src python packet* 
    ├── chat                -   *Chat module* 
    │   ├── __init__.py     -   *Initial chat python packet* 
    │   └── base.py         -   *Base chat python packet. Consists of base chat class* 
    ├── client              -   *Client's module* 
    │   ├── __init__.py     -   *Initial client python packet* 
    │   ├── base.py         -   *Base client python packet. Consists of base client class* 
    │   └── telegram.py     -   *Telegram client python packet* 
    ├── llm                 -   *LLM module* 
    │   ├── __init__.py     -   *Initial llm python packet* 
    │   ├── base.py         -   *Dabe LLM python packet. Consists of base LLM class* 
    │   └── mistral.py      -   *Mistral's python packet. Consists of Mistral API based class* 
    └── logger.py           -   *Python packet which consists of logger settings* 

*5 directories, 13 files* 
```

## Installation and launch:
### Instalation: 
```bash
git clone https://github.com/PATRUSOV/telegram-chan-agent.git
```
```bash
pip3 install -r requirements.txt
```
### Launch:
```bash
cd telegram-chan-agent
```
#### Put **your** API keys in **".env"** and then:
```bash
python3 main.py
```

# Russian:
# Telegram Chan Agent  
— это *AI‑агент* для Telegram‑аккаунта (и не только).

## Возможности агента (для Telegram)
- авторизация Telegram‑аккаунта  
- получение ID пользователей, от которых есть непрочитанные сообщения  
- получение непрочитанных сообщений по ID собеседника  
- пометка сообщений как прочитанных по ID собеседника  
- отправка сообщений по ID собеседника  
- обработка текста с помощью LLM API  
- поддержка асинхронного чата с собеседником  

## Структура репозитория
```
telegram-chan-agent/
├── main.py                 -   Точка входа в программу
├── .env                    -   Переменные окружения с вашими API-ключами
├── README.md               -   Этот файл
├── requirements.txt        -   Зависимости Python-программы
└── src                     -   Каталог с исходным кодом
    ├── __init__.py         -   Инициализирующий пакет src
    ├── chat                -   Модуль чата
    │   ├── __init__.py     -   Инициализирующий пакет chat
    │   └── base.py         -   Базовый модуль чата. Содержит базовый класс чата
    ├── client              -   Модуль клиента
    │   ├── __init__.py     -   Инициализирующий пакет client
    │   ├── base.py         -   Базовый клиентский модуль. Содержит базовый класс клиента
    │   └── telegram.py     -   Модуль Telegram‑клиента
    ├── llm                 -   Модуль LLM
    │   ├── __init__.py     -   Инициализирующий пакет llm
    │   ├── base.py         -   Базовый LLM‑модуль. Содержит базовый класс LLM
    │   └── mistral.py      -   Модуль Mistral. Класс на базе API Mistral
    └── logger.py           -   Модуль с настройками логгера

5 каталогов, 13 файлов
```

## Установка и запуск

### Установка
```bash
git clone https://github.com/PATRUSOV/telegram-chan-agent.git
pip3 install -r requirements.txt
```

### Запуск
```bash
cd telegram-chan-agent
```
#### Поместите **свои** API‑ключи в файл **`.env`**, затем выполните
```bash
python3 main.py
```
