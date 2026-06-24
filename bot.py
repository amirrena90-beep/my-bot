from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8905216177:AAHWPVFxT5LH5s4pVL514vr4ZsC3BrwQmzg"
CHANNEL_ID = "Mr721_m"


# بررسی عضویت
async def is_member(bot, user_id):
    try:
        member = await bot.get_chat_member(
            chat_id=CHANNEL_ID,
            user_id=user_id
        )

        return member.status in ["member", "administrator", "creator"]
    except:
        return False


# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not await is_member(context.bot, user_id):
        await update.message.reply_text(
            "❌ اول باید در کانال عضو شوی.\n"
            f"👉 {CHANNEL_ID}"
        )
        return

    await update.message.reply_text(
        "✅ خوش آمدی!\n"
        "یک عبارت بفرست:\n"
        "مثال: 5+3 یا 10-4"
    )


# محاسبه
def calculate(text):
    try:
        if "+" in text:
            a, b = text.split("+")
            return int(a) + int(b)

        if "-" in text:
            a, b = text.split("-")
            return int(a) - int(b)

        return "❌ فقط از + یا - استفاده کن"
    except:
        return "❌ خطا در ورودی"


# پیام‌ها
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not await is_member(context.bot, user_id):
        await update.message.reply_text("❌ اول عضو کانال شو")
        return

    text = update.message.text
    result = calculate(text)

    await update.message.reply_text(str(result))


# اجرا
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot is running...")
app.run_polling()