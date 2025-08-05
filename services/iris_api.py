import aiohttp
from config import IRIS_ID, IRIS_TOKEN


class IrisAPI:
    BASE_URL = "https://iris-tg.ru/api"

    def __init__(self, iris_id: str, iris_token: str):
        self.iris_id = iris_id
        self.iris_token = iris_token
        self.session = None

    async def _get_session(self):
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session

    async def _request(self, method: str, params: dict = None):
        params = params or {}
        url = f"{self.BASE_URL}/{self.iris_id}_{self.iris_token}/{method}"

        session = await self._get_session()

        try:
            async with session.get(url, params=params, ssl=False) as response:
                if response.status == 200:
                    try:
                        return await response.json()
                    except aiohttp.ContentTypeError:
                        text = await response.text()
                        raise Exception(f"Ошибка формата данных: {text}")
                else:
                    text = await response.text()
                    raise Exception(f"Ошибка запроса: {response.status} {text}")
        except Exception as e:
            raise Exception(f"Ошибка связи с IRIS API: {e}")


    async def balance(self):
        return await self._request("pocket/balance")

    async def give_sweets(self, user_id: int, sweets: int, comment: str = ""):
        params = {
            "user_id": user_id,
            "sweets": sweets,
            "comment": comment
        }
        return await self._request("pocket/sweets/give", params)


    async def history_sweets(self, offset: int = 0):
        params = {"offset": offset}
        return await self._request("pocket/sweets/history", params)

    async def give_gold(self, user_id: int, gold: int, comment: str = ""):
        params = {
            "user_id": user_id,
            "gold": gold,
            "comment": comment
        }
        return await self._request("pocket/gold/give", params)

    async def history_gold(self, offset: int = 0):
        params = {"offset": offset}
        return await self._request("pocket/gold/history", params)

    async def enable_pocket(self):
        return await self._request("pocket/enable")

    async def disable_pocket(self):
        return await self._request("pocket/disable")

    async def allow_user(self, user_id: int):
        params = {"user_id": user_id}
        return await self._request("pocket/allow_user", params)

    async def deny_user(self, user_id: int):
        params = {"user_id": user_id}
        return await self._request("pocket/deny_user", params)

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()


iris = IrisAPI(IRIS_ID, IRIS_TOKEN)
