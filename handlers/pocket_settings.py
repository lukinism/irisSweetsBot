from aiogram import types, Router
from aiogram.filters import Command
from services.iris_api import iris
from config import ADMIN_IDS

router = Router()

@router.message(Command("pocket_enable"))
async def cmd_pocket_enable(message: types.Message):
    await handle_simple_admin_command(
        message,
        iris.enable_pocket,
        success_text="✅ Теперь можно получать ириски и голду.",
        fail_text="Не удалось разрешить получение"
    )


@router.message(Command("pocket_disable"))
async def cmd_pocket_disable(message: types.Message):
    await handle_simple_admin_command(
        message,
        iris.disable_pocket,
        success_text="🛑 Получение ирисок и голды теперь запрещено.",
        fail_text="Не удалось отключить получение"
    )

async def handle_simple_admin_command(message: types.Message, api_method, success_text: str, fail_text: str
):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("❌ У вас нет прав использовать эту команду.")
        return

    try:
        result = await api_method()
        if result.get("response") == "ok":
            await message.answer(success_text)
        else:
            await message.answer(f"❌ {fail_text}: {result}")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")
