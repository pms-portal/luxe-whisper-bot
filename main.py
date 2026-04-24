import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI

# ✅ Env variables
TOKEN = os.getenv("BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

# ⚠️ Safety check (important)
if not TOKEN:
    raise Exception("BOT_TOKEN missing in environment variables")

if not OPENAI_KEY:
    raise Exception("OPENAI_API_KEY missing in environment variables")

client = OpenAI(api_key=OPENAI_KEY)

# Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✨ Welcome to Luxe Whisper AI Bot\n💬 Talk to me like a friend..."
    )

# AI reply
def ai_reply(user_text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are Luxe Whisper, a polite, slightly flirty luxury chatbot assistant."},
            {"role": "user", "content": user_text}
        ]
    )
    return response.choices[0].message.content

# Message handler
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        answer = ai_reply(user_text)
    except Exception as e:
        answer = f"⚠️ AI error: {str(e)}"

    await update.message.reply_text(answer)

# Bot setup
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

app.run_polling()
