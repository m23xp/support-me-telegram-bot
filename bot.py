import logging
from telegram import Update, LabeledPrice, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    PreCheckoutQueryHandler,
    filters,
    ContextTypes,
)

TOKEN = 'TOKEN'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_text = (
        f"مرحباً بك {user.first_name}! 👋\n\n"
        "أنا بوت مخصص لاستقبال الدعم لتطوير المحتوى والمشاريع القادمة. "
        "دعمكم يساعدني على الاستمرار وتقديم الأفضل دائماً. ❤️\n\n"
        "👇 **اختر باقة الدعم التي تناسبك:**"
    )

    keyboard = [
        [
            InlineKeyboardButton("⭐️ دعم بسيط (1 Star)", callback_data='buy_1'),
            InlineKeyboardButton("☕️ ثمن قهوة (5 Stars)", callback_data='buy_5')
        ],
        [
            InlineKeyboardButton("🚀 دعم كبير (50 Stars)", callback_data='buy_50'),
            InlineKeyboardButton("💎 دعم VIP (100 Stars)", callback_data='buy_100')
        ],
        [InlineKeyboardButton("🔗 زيارة قناتنا", url="https://t.me/username")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.edit_message_text(welcome_text, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    price = 0
    title = ""
    description = ""
    
    if data == 'buy_1':
        price = 1
        title = "دعم بسيط ⭐️"
        description = "شكراً لك! هذا الدعم يعني لي الكثير."
    elif data == 'buy_5':
        price = 5
        title = "ثمن قهوة ☕️"
        description = "شكراً على القهوة! ستساعدني في التركيز."
    elif data == 'buy_50':
        price = 50
        title = "دعم المميز 🚀"
        description = "دعم رائع! أنت تساهم بشكل كبير في التطوير."
    elif data == 'buy_100':
        price = 100
        title = "دعم VIP 💎"
        description = "أنت أسطورة! شكراً لدعمك اللامحدود."
    else:
        return

    chat_id = query.message.chat_id
    payload = f"support_{price}"
    currency = "XTR"
    prices = [LabeledPrice(title, int(price * 1))]

    await context.bot.send_invoice(
        chat_id=chat_id,
        title=title,
        description=description,
        payload=payload,
        provider_token="",
        currency=currency,
        prices=prices,
    )

async def precheckout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.pre_checkout_query
    if query.invoice_payload.startswith('support_'):
        await query.answer(ok=True)
    else:
        await query.answer(ok=False, error_message="حدث خطأ في معالجة الطلب.")

async def successful_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    payment = update.message.successful_payment
    amount = payment.total_amount
    
    thank_you_text = (
        f"✅ **تم استلام الدعم بنجاح!**\n\n"
        f"شكراً جزيلاً لك على دعمك بـ {amount} Star.\n"
        "بفضلك نستمر في العمل! ❤️"
    )
    
    await update.message.reply_text(thank_you_text)

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(PreCheckoutQueryHandler(precheckout_callback))
    application.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback))

    application.run_polling()

if __name__ == '__main__':
    main()
