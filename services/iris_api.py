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

    async def give_sweets(self, user_id: int, sweets: int, comment: str = ""):
        params = {
            "user_id": user_id,
            "sweets": sweets,
            "comment": comment
        }
        return await self._request("give_sweets", params)

    async def balance(self):
        return await self._request("balance")

    async def history(self, offset: int = 0):
        params = {"offset": offset}
        return await self._request("history", params)

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()


iris = IrisAPI(IRIS_ID, IRIS_TOKEN)
