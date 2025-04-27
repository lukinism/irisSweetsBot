from telethon import TelegramClient
from config import API_ID, API_HASH


class TelethonClient:
    def __init__(self):
        self.client = TelegramClient('telethon_session', API_ID, API_HASH)

    async def start(self):
        await self.client.start()

    async def stop(self):
        await self.client.disconnect()

    async def get_user_info(self, username: str):
        entity = await self.client.get_entity(username)
        return entity.id, entity.username, entity.first_name, entity.last_name


telethon_client = TelethonClient()
