import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI

# ✅ Railway variables থেকে load হবে
TOKEN = os.getenv("BOT_TOKEN")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✨ Welcome to Luxe Whisper AI Bot\n💬 Talk to me like a friend..."
    )

# AI reply
async def ai_reply(user_text):
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
        answer = await ai_reply(user_text)
    except Exception:
        answer = "⚠️ AI server error, please try again."

    await update.message.reply_text(answer)

# Bot setup
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

app.run_polling()
