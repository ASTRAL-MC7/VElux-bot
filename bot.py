import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "YOUR_BOT_TOKEN"
ADMIN_ID = 5523761749
CHANNEL = "vaelux"

bot = Bot(token=TOKEN)
dp = Dispatcher()

users = set()  # simple storage (keyin DB qilsa bo‘ladi)


# ---------------- START ----------------
@dp.message(Command("start"))
async def start(msg: types.Message):
    user_id = msg.from_user.id
    username = msg.from_user.first_name

    try:
        member = await bot.get_chat_member(f"@{CHANNEL}", user_id)
        if member.status in ["left", "kicked"]:
            raise Exception()
    except:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📢 Kanalga a’zo bo‘lish", url="https://t.me/vaelux")]
        ])
        await msg.answer(
            f"👋 Salom {username}!\n\n"
            "🚀 Vaelux botdan to‘liq foydalanish uchun kanalga a’zo bo‘lishingiz shart!\n"
            "💡 Biz sizga eng zamonaviy bot tizimlarini yaratishda yordam beramiz.",
            reply_markup=kb
        )
        return

    users.add(user_id)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌐 Websaytga o‘tish", url="https://astral-mc7.github.io/VAelux-main/")]
    ])

    await msg.answer(
        f"🎉 Xush kelibsiz {username}!\n\n"
        "🤖 Siz endi Vaelux ekotizimining a’zosiz!\n"
        "⚡ G‘oyangizni real botga aylantirish imkoniyati endi sizda!\n\n"
        "👇 Davom etish uchun pastdagi tugmani bosing.",
        reply_markup=kb
    )


# ---------------- HELP ----------------
@dp.message(Command("help"))
async def help_cmd(msg: types.Message):
    await msg.answer(
        "📘 *Vaelux Bot Yordam*\n\n"
        "📌 /start — botni ishga tushirish\n"
        "📌 Kanalga a’zo bo‘lish shart\n"
        "📌 Obuna bo‘lsangiz — websayt ochiladi\n\n"
        "🚀 Imkoniyatlar:\n"
        "• 🤖 Bot g‘oyasini yuborish\n"
        "• 🎮 GameHub kirish\n"
        "• ⚡ tez avtomatlashtirish\n\n"
        "💡 Vaelux — g‘oyalaringizni tizimga aylantiruvchi platforma.",
        parse_mode="Markdown"
    )


# ---------------- PANEL ----------------
@dp.message(Command("panel"))
async def panel(msg: types.Message):
    if msg.from_user.id != ADMIN_ID:
        return await msg.answer("❌ Sizda ruxsat yo‘q!")

    await msg.answer(
        "👑 ADMIN PANEL\n\n"
        "📊 /odam — foydalanuvchilar soni\n"
        "📢 /xabar <matn> — hammaga yuborish\n"
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

    await msg.answer("✅ Xabar yuborildi!")


# ---------------- RUN ----------------
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())