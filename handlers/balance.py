from aiogram import types, Router
from aiogram.filters import Command
from services.iris_api import iris

router = Router()


@router.message(Command("balance"))
async def cmd_balance(message: types.Message):
    try:
        data = await iris.balance()
        gold = data.get("gold", "Не удалось получить голду")
        sweets = data.get("sweets", "Не удалось получить ириски")
        donate_score = data.get("donate_score", "Не удалось получить очки доната")

        await message.answer(
            f"📊 *Ваш баланс:*\n\n"
            f"🌕 Голда: {gold}\n"
            f"🍬 Ириски: {sweets}\n"
            f"🎖 Донатные очки: {donate_score}",
            parse_mode="Markdown"
        )
    except Exception as e:
        await message.answer(f"❌ Ошибка при получении баланса: {e}")
