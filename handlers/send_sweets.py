from aiogram import types, Router
from aiogram.filters import Command, CommandObject
from services.telethon_client import telethon_client
from services.utils import get_iriski_word, get_otpravleno_word
from services.iris_api import iris
from config import ADMIN_IDS

router = Router()


@router.message(Command("send_sweets"))
async def cmd_send_sweets(message: types.Message, command: CommandObject):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("❌ У вас нет прав использовать эту команду.")
        return

    if not command.args:
        await message.answer(
            "❗ Укажите количество и @username или @user_id.\n\nПример:\n`/send_sweets 10 @lukinism`\nКомментарий с "
            "новой строки (необязательно)",
            parse_mode="Markdown")
        return

    lines = command.args.strip().split('\n')
    first_line = lines[0].strip()
    comment = "\n".join(lines[1:]).strip() if len(lines) > 1 else "Без комментария"

    parts = first_line.split()
    if len(parts) != 2:
        await message.answer(
            "❗ Неверный формат.\nДолжно быть: количество и @username/@user_id через пробел.",
            parse_mode="Markdown")
        return

    try:
        sweets_count = int(parts[0])
        user_input = parts[1]

        if not user_input.startswith("@"):
            await message.answer("❗ Username или ID должен начинаться с '@'.", parse_mode="Markdown")
            return

        user_ref = user_input[1:]

        if user_ref.isdigit():
            user_id = int(user_ref)
            display_name = f"ID {user_id}"
        else:
            try:
                user_id, username, first_name, last_name = await telethon_client.get_user_info(user_ref)
                print(user_id, username)
                display_name = f"@{username}" if username else f"{first_name or ''} {last_name or ''}".strip()
            except Exception as e:
                await message.answer(f"❌ Не удалось найти пользователя {user_input}.\nОшибка: {e}")
                return

    except ValueError:
        await message.answer("❗ Количество ирисок должно быть числом.", parse_mode="Markdown")
        return

    try:
        result = await iris.give_sweets(
            user_id=user_id,
            sweets=sweets_count,
            comment=comment
        )

        if "error" in result:
            error_description = result["error"].get("description", "Неизвестная ошибка")
            await message.answer(f"❌ Ошибка при отправке ирисок: {error_description}")
        else:
            await message.answer(
                f"✅ {get_otpravleno_word(sweets_count)} {sweets_count} {get_iriski_word(sweets_count)} пользователю {display_name}.\n\n"
                f"💬 Комментарий:\n{comment}",
                parse_mode="Markdown"
            )
    except Exception as e:
        await message.answer(f"❌ Системная ошибка при отправке ирисок: {e}")
