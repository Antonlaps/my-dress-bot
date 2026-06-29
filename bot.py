import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ------ ВСТАВ СВОЇ ДАНІ ------
TELEGRAM_TOKEN = "AQ.Ab8RN6IlmOr7_xPig4EwpArCgbDmZRcVD1eXBxuhzNKBOkcY9g"
GEMINI_API_KEY = "8701998323:AAHASLziqrKX97YlUs35lCMoRslVAvpCN2Y"
# --------------------------------

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

TEMPLATE = """
Ти — експерт з одягу. Подивись на фото і заповни поля строго по порядку, коротко:

Вид виробу: 
Тип тканини: 
Фасон сукні: 
Розмір жіночого одягу (UA): 
Обхват грудей (см): 
Обхват талії (см): 
Стиль: 
Сезон: 
Фасон вирізу горловини: 
Фасон рукава: 
Склад: 
Властивості тканини: 
Візерунки і принти: 
Оброблення та прикраси: 
Довжина сукні: 
Довжина рукава: 
Наявність корсету: 
Шлейф: 
Країна виробник: 
Стан: 
Застібка: 
Наявність кишень:
"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Надішли мені фото плаття, я заповню шаблон!")


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = await update.message.photo[-1].get_file()
    await photo.download_to_drive('dress.jpg')

    await update.message.reply_text("Аналізую... зачекай секунду")

    try:
        img = open('dress.jpg', 'rb')
        response = model.generate_content([TEMPLATE, img])
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"Помилка: {e}")
    finally:
        os.remove('dress.jpg')


def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("Бот працює...")
    app.run_polling()


if __name__ == "__main__":
    main()