import asyncio
from aiohttp import web

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8637648331:AAGF7LcqJhXtDIVdfbzNCO1z0wMhDbOnVRQ"
ADMIN_ID = 5523761749
CHANNEL = "vaelux"

bot = Bot(token=TOKEN)
dp = Dispatcher()

users = set()

# ---------------- WEB SERVER ----------------
async def handle(request):
    return web.Response(text="Vaelux Bot is running 🚀")

async def run_web():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 10000)
    await site.start()

# ---------------- START ----------------
@dp.message(Command("start"))
async def start(msg: types.Message):
    user = msg.from_user
    username = user.first_name

    try:
        member = await bot.get_chat_member(f"@{CHANNEL}", user.id)
        if member.status in ["left", "kicked"]:
            raise Exception()
    except:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📢 Kanalga a’zo bo‘lish", url="https://t.me/vaelux")]
        ])
        await msg.answer(
            f"👋 Assalomu alaykum {username}!\n\n"
            "🚀 Botdan to‘liq foydalanish uchun kanalga a’zo bo‘lishingiz shart!\n"
            "⚡ Vaelux — g‘oyalaringizni real tizimga aylantiruvchi platforma.",
            reply_markup=kb
        )
        return

    users.add(user.id)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌐 Websayt", url="https://astral-mc7.github.io/VAelux-main/")]
    ])

    await msg.answer(
        f"🎉 Xush kelibsiz {username}!\n\n"
        "🤖 Siz Vaelux ekotizimiga muvaffaqiyatli qo‘shildingiz!\n"
        "🚀 Endi siz g‘oyalaringizni real botga aylantira olasiz!",
        reply_markup=kb
    )

# ---------------- HELP ----------------
@dp.message(Command("help"))
async def help_cmd(msg: types.Message):
    await msg.answer(
        "📘 Vaelux Yordam\n\n"
        "📌 /start — botni ishga tushirish\n"
        "📌 Kanalga obuna bo‘lish shart\n"
        "📌 Obuna bo‘lgach asosiy menyu ochiladi\n\n"
        "⚡ Imkoniyatlar:\n"
        "• Bot g‘oya yaratish\n"
        "• Websaytga kirish\n"
        "• Vaelux GameHub\n\n"
        "💡 Vaelux — g‘oyadan tizimgacha."
    )

# ---------------- PANEL ----------------
@dp.message(Command("panel"))
async def panel(msg: types.Message):
    if msg.from_user.id != ADMIN_ID:
        return await msg.answer("❌ Ruxsat yo‘q!")

    await msg.answer(
        "👑 ADMIN PANEL\n\n"
        "/odam — userlar soni\n"
        "/xabar <matn> — broadcast"
    )

# ---------------- USERS COUNT ----------------
@dp.message(Command("odam"))
async def odam(msg: types.Message):
    if msg.from_user.id != ADMIN_ID:
        return
    await msg.answer(f"📊 Start bosganlar: {len(users)} ta")

# ---------------- BROADCAST ----------------
@dp.message(Command("xabar"))
async def xabar(msg: types.Message):
    if msg.from_user.id != ADMIN_ID:
        return

    text = msg.text.replace("/xabar", "").strip()
    if not text:
        return await msg.answer("❌ Matn yozing!")

    for u in users:
        try:
            await bot.send_message(u, f"📢 {text}")
        except:
            pass

    await msg.answer("✅ Yuborildi!")

# ---------------- MAIN ----------------
async def main():
    await asyncio.gather(
        dp.start_polling(bot),
        run_web()
    )

if __name__ == "__main__":
    asyncio.run(main())
