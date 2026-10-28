import os
import json
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# Logging sozlamalari
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Render'dagi Environment variables'dan Admin ID ni o'qib olamiz
ADMIN_ID_STR = os.getenv("ADMIN_ID", "0")
try:
    ADMIN_ID = int(ADMIN_ID_STR)
except ValueError:
    ADMIN_ID = 0

# /start buyrug'i
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Kino kodi yoki nomini yuboring:")

# /admin buyrug'i (Faqat admin uchun ishlaydi)
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # Faqat ADMIN_ID ga ruxsat berish
    if user_id != ADMIN_ID:
        await update.message.reply_text("⛔ Sizda bu buyruqdan foydalanish huquqi yo'q!")
        return

    # Admin uchun menyu
    keyboard = [
        [InlineKeyboardButton("📊 Statistika", callback_data="admin_stats")],
        [InlineKeyboardButton("➕ Kino qo'shish (Ko'rsatma)", callback_data="admin_add_info")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🎛 <b>Xush kelibsiz, Admin!</b>\nAdmin paneliga kirdingiz. Kerakli amalni tanlang:",
        reply_markup=reply_markup,
        parse_mode="HTML"
    )

# Admin tugmalari bosilganda
async def admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    if user_id != ADMIN_ID:
        await query.answer("Siz admin emassiz!", show_alert=True)
        return

    await query.answer()

    if query.data == "admin_stats":
        await query.edit_message_text("📊 Bot statistikasi:\n\n• Hozircha hamma narsa sozlanmoqda.")
    elif query.data == "admin_add_info":
        await query.edit_message_text("➕ Kino qo'shish uchun `catalog.json` faylini GitHub'da tahrirlashingiz mumkin.")

# Kino qidirish funksiyasi
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    # Catalog.json faylidan kinolarni o'qish
    try:
        with open("catalog.json", "r", encoding="utf-8") as f:
            catalog = json.load(f)
    except Exception as e:
        catalog = {}

    if text in catalog:
        await update.message.reply_text(f"🎬 Topilgan kino: {catalog[text]}")
    else:
        await update.message.reply_text("❌ Kechiras
