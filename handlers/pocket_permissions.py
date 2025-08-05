from aiogram import types, Router
from aiogram.filters import Command, CommandObject
from services.telethon_client import telethon_client
from services.iris_api import iris
from config import ADMIN_IDS

router = Router()


@router.message(Command("allow_user"))
async def cmd_allow_user(message: types.Message, command: CommandObject):
    await handle_permission_command(
        message=message,
        command=command,
        action="allow",
        api_method=iris.allow_user,
        expected_response=True,
        success_text="✅ Пользователь {display_name} теперь *может* отправлять вам ириски-голду.",
        fail_text="Не удалось разрешить получение"
    )


@router.message(Command("deny_user"))
async def cmd_deny_user(message: types.Message, command: CommandObject):
    await handle_permission_command(
        message=message,
        command=command,
        action="deny",
        api_method=iris.deny_user,
        expected_response=False,
        success_text="🛑 Пользователь {display_name} теперь *не может* отправлять вам ириски-голду.",
        fail_text="Не удалось запретить получение"
    )



async def handle_permission_command(message: types.Message, command: CommandObject, action: str, api_method, expected_response: bool, success_text: str, fail_text: str
):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("❌ У вас нет прав использовать эту команду.")
        return

    if not command.args:
        await message.answer(
            f"❗ Укажите ID или @username пользователя.\nПример: `/{action}_user @lukinism`",
            parse_mode="Markdown"
        )
        return

    try:
        user_id, display_name = await resolve_user_id_and_display_name(command.args.strip())
        result = await api_method(user_id)

        if result.get("response") is expected_response:
            await message.answer(success_text.format(display_name=display_name), parse_mode="Markdown")
        else:
            await message.answer(f"⚠️ {fail_text}. Ответ: {result}")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")


async def resolve_user_id_and_display_name(user_input: str):
    user_ref = user_input[1:] if user_input.startswith("@") else user_input

    if user_ref.isdigit():
        user_id = int(user_ref)
        display_name = f"ID {user_id}"
    else:
        user_id, username, first_name, last_name = await telethon_client.get_user_info(user_ref)
        display_name = f"@{username}" if username else f"{first_name or ''} {last_name or ''}".strip()

    return user_id, display_name


