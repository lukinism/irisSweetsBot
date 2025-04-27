# IrisSweetsBot — Бот для работы с IRIS API через Telegram

Этот бот позволяет работать с системой IRIS API для отправки ирисок другим пользователям, просмотра баланса и истории транзакций.

---

## 🚀 Возможности

- `/balance` — Показать текущий баланс ирисок и донатных очков.
- `/send_sweets [кол-во] [@username или @user_id]` + комментарий (с новой строки) — Отправить ириски любому пользователю с возможностью указать комментарий.
- `/history [offset]` — Просмотреть историю последних операций.

---

## 📦 Установка

1. Клонируйте репозиторий:

```bash
git clone https://github.com/lukinism/irisbot.git
cd irisbot
```

2. Установите зависимости:

```bash
pip install -r requirements.txt
```

3. В файл `config.py` добавьте свои настройки:

```python
BOT_TOKEN = "ВАШ_ТОКЕН_Бота"
IRIS_ID = "ВАШ_IRIS_ID"
IRIS_TOKEN = "ВАШ_IRIS_TOKEN"

API_ID = "ВАШ_API_ID"
API_HASH = "ВАШ_API_HASH"

ADMIN_IDS = [ваш_telegram_id]
```

4. Запустите бота:

```bash
python bot.py
```

---

## ⚙️ Требования

- Python 3.9+
- aiohttp
- aiogram 3
- telethon

---

## 🛠 Используемые технологии

- [aiogram 3](https://docs.aiogram.dev/en/latest/)
- [telethon](https://docs.telethon.dev/en/stable/)
- [aiohttp](https://docs.aiohttp.org/en/stable/)

---

## 🛡 Права доступа

Команду `/send_sweets` могут использовать только администраторы, указанные в файле `config.py` в списке `ADMIN_IDS`.

```python
ADMIN_IDS = [1, 2]
```

---

## 📜 Примеры использования команд

**Проверка баланса:**

```
/balance
```

**Отправка ирисок пользователю:**

```
/send_sweets 10 @username
Комментарий к оплате
```

**Просмотр истории операций:**

```
/history 0
```

---

## 🛡 Обработка ошибок

Бот обрабатывает:

- Нехватку ирисок
- Неверный формат команд
- Ошибки сети
- Ошибки поиска пользователей

---

## 📜 Лицензия

Проект распространяется под лицензией **MIT**.

---

## 📞 Контакты

**Разработчик:** [@lukinism](https://t.me/lukinism)