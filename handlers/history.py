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
    args = (command.args or "").strip().split()

    if not args or args[0] not in ["sweets", "gold"]:
        await message.answer(
            "❗ Укажите, что показать: `sweets` или `gold`.\n\nПримеры:\n"
            "`/history sweets`\n`/history gold 5` (с offset)",
            parse_mode="Markdown"
        )
        return

    resource_type = args[0]  # sweets / gold
    offset = 0

    if len(args) == 2:
        try:
            offset = int(args[1])
            if offset < 0:
                raise ValueError
        except ValueError:
            await message.answer("❗ Offset должен быть положительным числом.", parse_mode="Markdown")
            return

    try:
        if resource_type == "sweets":
            data = await iris.history_sweets(offset=offset)
            icon = "🍬"
            resource_title = "ирисок"
        else:
            data = await iris.history_gold(offset=offset)
            icon = "🪙"
            resource_title = "золота"

        if not data:
            await message.answer(f"📜 История {resource_title} пуста.")
            return

        text = f"📜 *История {resource_title} (offset {offset}):*\n\n"

        for item in data[:5]:
            amount = item.get("amount", "неизвестно")
            action_type = item.get("type", "неизвестно")
            readable_action = ACTION_TYPES.get(action_type, action_type)

            timestamp = item.get("date", 0) // 1000
            dt = datetime.fromtimestamp(timestamp)
            formatted_date = dt.strftime("%d.%m.%Y %H:%M")

            text += f"• {formatted_date} | {readable_action} | {amount} {icon}\n"

        await message.answer(text, parse_mode="Markdown")

    except Exception as e:
        await message.answer(f"❌ Ошибка при получении истории: {e}")
