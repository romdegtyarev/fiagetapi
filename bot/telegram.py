import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram import F
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile
from aiogram.client.default import DefaultBotProperties

from dotenv import load_dotenv

from logic.session_loader import load_session
from logic.best_laps import generate_best_laps_image, generate_laptime_distribution_image
from logic.results import generate_results_image, export_results_csv
from logic.position_changes import generate_position_changes_image
from logic.strategy import generate_strategy_image
from logic.driver_styling import generate_driver_styling_image
from logic.db import create_users_table, add_user, list_users, is_user_exists


load_dotenv()


TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_ADMIN_ID = int(os.getenv("TELEGRAM_ADMIN_ID", "0"))


bot = Bot(
    token=TELEGRAM_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
)
dp = Dispatcher()


@dp.startup()
async def on_startup(bot):
    await create_users_table()
    print("DB tables created.")


@dp.message(F.text.startswith("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я F1 бот. Доступные команды:\n"
        "best_laps <год> <gp> <тип>\n"
        "results <год> <gp> <тип>\n"
        "position_changes <год> <gp> <тип>\n"
        "strategy <год> <gp> <тип>\n"
        "driver_styling <год> <gp> <тип> <driver>\n"
        "Пример: best_laps 2024 Monaco R\n"
        "Для driver_styling: driver_styling 2024 Monaco R LEC\n"
    )


@dp.message(F.text.startswith("add_user"))
async def add_user_cmd(message: types.Message):
    if message.from_user.id != TELEGRAM_ADMIN_ID:
        await message.answer("❌ Нет прав.")
        return
    args = message.text.strip().split()
    if len(args) < 2:
        await message.answer("Формат: /add_user <user_id>")
        return
    try:
        user_id = int(args[1])
        username = ""
        if message.reply_to_message:
            username = message.reply_to_message.from_user.username or ""
        await add_user(user_id, username)
        await message.answer(f"✅ Пользователь {user_id} добавлен.")
    except Exception as e:
        await message.answer(f"Ошибка: {e}")


@dp.message(F.text.startswith("list_users"))
async def list_users_cmd(message: types.Message):
    if message.from_user.id != TELEGRAM_ADMIN_ID:
        await message.answer("❌ Нет прав.")
        return
    rows = await list_users()
    if not rows:
        await message.answer("❌ Нет пользователей.")
    else:
        text = "\n".join(
            f"{r['user_id']} — {r['username'] or '-'} ({r['date_added'].strftime('%Y-%m-%d')})"
            for r in rows
        )
        await message.answer(text)


def parse_args(text: str, need_driver: bool = False):
    try:
        args = text.strip().split()
        year = int(args[1])
        gp = args[2]
        sess_type = args[3].upper()
        driver = args[4].upper() if need_driver and len(args) > 4 else None
        return year, gp, sess_type, driver
    except Exception:
        return None, None, None, None

async def is_allowed(user_id: int) -> bool:
    return (user_id == TELEGRAM_ADMIN_ID) or await is_user_exists(user_id)


async def check_and_run(handler, message, need_driver=False):
    user_id = message.from_user.id
    if not await is_allowed(user_id):
        await message.answer("❌ Нет доступа. Обратитесь к администратору.")
        return
    year, gp, sess_type, driver = parse_args(message.text, need_driver=need_driver)
    if not all([year, gp, sess_type]) or (need_driver and not driver):
        await message.answer("❌ Формат команды некорректен.")
        return
    await handler(message, year, gp, sess_type, driver)


@dp.message(F.text.startswith("best_laps"))
async def best_laps_cmd(message: types.Message):
    async def handler(msg, year, gp, sess_type, driver):
        try:
            session = load_session(year, gp, sess_type)
            path1 = generate_best_laps_image(session)
            path2 = generate_laptime_distribution_image(session)
            await msg.answer_photo(FSInputFile(path1), caption="Best Laps")
            await msg.answer_photo(FSInputFile(path2), caption="Laptime Distribution")
        except Exception as e:
            await msg.answer(f"Ошибка: {e}")
    await check_and_run(handler, message)


@dp.message(F.text.startswith("results"))
async def results_cmd(message: types.Message):
    async def handler(msg, year, gp, sess_type, driver):
        try:
            session = load_session(year, gp, sess_type)
            path = generate_results_image(session)
            await msg.answer_photo(FSInputFile(path), caption="Session Results")
            csv_path = export_results_csv(session)
            await msg.answer_document(FSInputFile(csv_path), caption="CSV")
        except Exception as e:
            await msg.answer(f"Ошибка: {e}")
    await check_and_run(handler, message)


@dp.message(F.text.startswith("position_changes"))
async def position_cmd(message: types.Message):
    async def handler(msg, year, gp, sess_type, driver):
        try:
            session = load_session(year, gp, sess_type)
            path = generate_position_changes_image(session)
            await msg.answer_photo(FSInputFile(path), caption="Position Changes")
        except Exception as e:
            await msg.answer(f"Ошибка: {e}")
    await check_and_run(handler, message)


@dp.message(F.text.startswith("strategy"))
async def strategy_cmd(message: types.Message):
    async def handler(msg, year, gp, sess_type, driver):
        try:
            session = load_session(year, gp, sess_type)
            path = generate_strategy_image(session)
            await msg.answer_photo(FSInputFile(path), caption="Tire Strategy")
        except Exception as e:
            await msg.answer(f"Ошибка: {e}")
    await check_and_run(handler, message)


@dp.message(F.text.startswith("driver_styling"))
async def driver_styling_cmd(message: types.Message):
    async def handler(msg, year, gp, sess_type, driver):
        try:
            session = load_session(year, gp, sess_type)
            path = generate_driver_styling_image(session, driver)
            await msg.answer_photo(FSInputFile(path), caption=f"Driver {driver} Lap Styling")
        except Exception as e:
            await msg.answer(f"Ошибка: {e}")
    await check_and_run(handler, message, need_driver=True)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(dp.start_polling(bot))
