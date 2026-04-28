import asyncio
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8637648331:AAGF7LcqJhXtDIVdfbzNCO1z0wMhDbOnVRQ"
CHANNEL = "vaelux"
ADMIN_ID = 5523761749

# -------- LOG OPTIMIZATION --------
logging.basicConfig(level=logging.ERROR)

# -------- BOT --------
bot = Bot(token=TOKEN)
dp = Dispatcher()

user_count = 0
seen_users = set()  # faqat count uchun

# -------- LOG CLEANER --------
async def clear_logs():
    while True:
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        logging.basicConfig(level=logging.ERROR)
        await asyncio.sleep(60)

# -------- WEB SERVER --------
async def handle(request):
    return web.Response(text="Vaelux running 🚀")

async def run_web():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 10000)
    await site.start()

# -------- START --------
@dp.message(Command("start"))
async def start(msg: types.Message):
    global user_count

    user_id = msg.from_user.id
    name = msg.from_user.first_name

    # user count only
    if user_id not in seen_users:
        seen_users.add(user_id)
        user_count += 1

    # kanal check
    try:
        member = await bot.get_chat_member(f"@{CHANNEL}", user_id)
        if member.status in ["left", "kicked"]:
            raise Exception()
    except:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📢 Kanalga a’zo bo‘lish", url="https://t.me/vaelux")],
            [InlineKeyboardButton(text="✅ Tekshirish", callback_data="check")]
        ])
        await msg.answer(
            f"👋 Assalomu alaykum {name}!\n\n"
            "⚠️ Botdan foydalanish uchun kanalga a’zo bo‘ling!\n"
            "🚀 Vaelux — g‘oyani real tizimga aylantiradi.",
            reply_markup=kb
        )
        return

    await success(msg)

# -------- CALLBACK CHECK --------
@dp.callback_query(lambda c: c.data == "check")
async def check_sub(call: types.CallbackQuery):
    user_id = call.from_user.id

    try:
        member = await bot.get_chat_member(f"@{CHANNEL}", user_id)
        if member.status in ["left", "kicked"]:
            raise Exception()
    except:
        return await call.answer("❌ Hali a’zo emassiz!", show_alert=True)

    await success(call.message)
    await call.answer()

# -------- SUCCESS --------
async def success(msg):
    name = msg.from_user.first_name

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌐 WEBSAYT", url="https://astral-mc7.github.io/VAelux-main/")]
    ])

    await msg.answer(
        f"🎉 {name}, siz muvaffaqiyatli qo‘shildingiz!\n\n"
        "🚀 Endi Vaelux tizimidan foydalanishingiz mumkin!\n"
        "⚡ G‘oyangizni real botga aylantiring.",
        reply_markup=kb
    )

# -------- HELP --------
@dp.message(Command("help"))
async def help_cmd(msg: types.Message):
    await msg.answer(
        "📘 Vaelux yordam\n\n"
        "/start — boshlash\n"
        "Kanalga a’zo bo‘lish shart\n\n"
        "🚀 Vaelux — g‘oyadan tizimgacha"
    )

# -------- ADMIN --------
@dp.message(Command("panel"))
async def panel(msg: types.Message):
    if msg.from_user.id != ADMIN_ID:
        return
    await msg.answer(
        "👑 ADMIN PANEL\n\n"
        "/odam — user count"
    )

@dp.message(Command("odam"))
async def odam(msg: types.Message):
    if msg.from_user.id != ADMIN_ID:
        return
    await msg.answer(f"📊 Users: {user_count}")

# -------- MAIN --------
async def main():
    await asyncio.gather(
        dp.start_polling(bot),
        run_web(),
        clear_logs()
    )

if __name__ == "__main__":
    asyncio.run(main())
