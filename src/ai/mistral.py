import os
import json
import dotenv
from typing import List, Dict, Optional
from mistralai import Mistral

dotenv.load_dotenv()


class MistralClient:
    def __init__(
        self, api_key: Optional[str] = None, model: str = "mistral-large-latest"
    ):
        self.api_key = api_key or os.environ.get("MISTRAL_API_KEY")
        if not self.api_key:
            raise RuntimeError("MISTRAL_API_KEY is not set")
        self.model = model
        self.client = Mistral(api_key=self.api_key)

    def complete(self, messages: List[Dict[str, str]]) -> str:
        response = self.client.chat.complete(model=self.model, messages=messages)
        return response.choices[0].message.content


class ChatSession:
    def __init__(
        self, mistral_client: MistralClient, history_file: Optional[str] = None
    ):
        self.client = mistral_client
        self.messages: List[Dict[str, str]] = []
        self.history_file = history_file
        if self.history_file:
            self._load()

    def set_system_prompt(self, content: str):
        self.messages.insert(0, {"role": "system", "content": content})

    def send(self, user_input: str) -> str:
        self.messages.append({"role": "user", "content": user_input})
        reply = self.client.complete(self.messages)
        self.messages.append({"role": "assistant", "content": reply})
        if self.history_file:
            self._save()
        return reply

    def reset(self):
        self.messages = []
        if self.history_file:
            try:
                os.remove(self.history_file)
            except FileNotFoundError:
                pass

    def _save(self):
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(self.messages, f, indent=2, ensure_ascii=False)

    def _load(self):
        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                self.messages = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.messages = []
