from aiogram import types, Router
from aiogram.filters import Command, CommandObject
from services.telethon_client import telethon_client
from services.utils import get_otpravleno_word
from services.iris_api import iris
from config import ADMIN_IDS

router = Router()

@router.message(Command("send_gold"))
async def cmd_send_gold(message: types.Message, command: CommandObject):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("❌ У вас нет прав использовать эту команду.")
        return

    if not command.args:
        await message.answer(
            "❗ Укажите количество и @username или ID.\n\nПример:\n`/send_gold 5 @lukinism`\nКомментарий с новой строки (необязательно)",
            parse_mode="Markdown")
        return

    lines = command.args.strip().split('\n')
    first_line = lines[0].strip()
    comment = "\n".join(lines[1:]).strip() if len(lines) > 1 else "Без комментария"

    parts = first_line.split()
    if len(parts) != 2:
        await message.answer(
            "❗ Неверный формат.\nДолжно быть: количество и @username/ID через пробел.",
            parse_mode="Markdown")
        return

    try:
        gold_count = int(parts[0])
        if gold_count <= 0:
            await message.answer("❗ Количество голды должно быть положительным числом.")
            return

        user_input = parts[1]
        user_ref = user_input[1:] if user_input.startswith("@") else user_input

        if user_ref.isdigit():
            user_id = int(user_ref)
            display_name = f"ID {user_id}"
        else:
            try:
                user_id, username, first_name, last_name = await telethon_client.get_user_info(user_ref)
                display_name = f"@{username}" if username else f"{first_name or ''} {last_name or ''}".strip()
            except Exception as e:
                await message.answer(f"❌ Не удалось найти пользователя {user_input}.\nОшибка: {e}")
                return

    except ValueError:
        await message.answer("❗ Количество должно быть числом.", parse_mode="Markdown")
        return

    try:
        result = await iris.give_gold(
            user_id=user_id,
            gold=gold_count,
            comment=comment
        )

        if "error" in result:
            error_description = result["error"].get("description", "Неизвестная ошибка")
            await message.answer(f"❌ Ошибка при отправке голды: {error_description}")
        else:
            comment_text = f"\n\n💬 Комментарий:\n{comment}" if comment != "Без комментария" else ""
            await message.answer(
                f"✅ {get_otpravleno_word(gold_count)} {gold_count} голд пользователю {display_name}.{comment_text}",
                parse_mode="Markdown"
            )
    except Exception as e:
        await message.answer(f"❌ Системная ошибка при отправке голды: {e}")
