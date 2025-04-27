from aiogram import types, Router
from aiogram.filters import Command, CommandObject
from services.iris_api import iris
from datetime import datetime

ACTION_TYPES = {
    "send": "Отправил",
    "take": "Получил",
}

router = Router()


@router.message(Command("history"))
async def cmd_history(message: types.Message, command: CommandObject):
    args = command.args
    offset = 0

    if args:
        try:
            offset = int(args.strip())
            if offset < 0:
                raise ValueError
        except ValueError:
            await message.answer(
                "❗ Offset должен быть положительным числом.\n\nПример:\n`/history 0` или `/history 10`",
                parse_mode="Markdown"
            )
            return

    try:
        data = await iris.history(offset=offset)

        if not data:
            await message.answer("📜 История пуста.")
            return

        text = f"📜 *История операций (offset {offset}):*\n\n"

        for item in data[:5]:
            amount = item.get("amount", "неизвестно")
            action_type = item.get("type", "неизвестно")
            readable_action = ACTION_TYPES.get(action_type, action_type)

            timestamp = item.get("date", 0) // 1000
            dt = datetime.fromtimestamp(timestamp)
            formatted_date = dt.strftime("%d.%m.%Y %H:%M")

            text += f"• {formatted_date} | {readable_action} | {amount} 🍬\n"

        await message.answer(text, parse_mode="Markdown")

    except Exception as e:
        await message.answer(f"❌ Ошибка при получении истории: {e}")
