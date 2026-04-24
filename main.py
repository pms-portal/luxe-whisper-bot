import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI

TOKEN = os.getenv("7971330904:AAFFCUbULvRTIekStIEdiAInXR2bCjRM0wA")
client = OpenAI(api_key=os.getenv("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"))

# Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✨ Welcome to Luxe Whisper AI Bot\n Talk to me like a friend..."
    )

# AI reply function
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
