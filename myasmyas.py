from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# Замените этим ID вашего канала
CHANNEL_ID = -1002433952702

# Определите состояния
NAME, PHONE, ADDRESS, PET_INFO, DRIED_PRODUCTS, PASTILA, COOKIES, OTHER_PRODUCTS, GIFT, PACKAGING = range(10)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Привіт! Я допоможу вам зробити замовлення. Почнемо з інформації про клієнта.\n\n"
        "Введіть ПІБ:"
    )
    return NAME

async def get_client_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message and update.message.text:
        context.user_data['name'] = update.message.text
        await update.message.reply_text("Введіть мобільний номер:")
        return PHONE
    else:
        await update.message.reply_text("Будь ласка, введіть текстове повiдомлення.")
        return NAME

async def get_client_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message and update.message.text:
        context.user_data['phone'] = update.message.text
        await update.message.reply_text("Введіть дані для відправки (місто, відділення/поштомат):")
        return ADDRESS
    else:
        await update.message.reply_text("Будь ласка, введіть текстове повiдомлення.")
        return PHONE

async def get_client_address(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message and update.message.text:
        context.user_data['address'] = update.message.text
        await update.message.reply_text("Введіть інформацію про улюбленця (Прізвисько, порода, вага, протипоказання):")
        return PET_INFO
    else:
        await update.message.reply_text("Будь ласка, введіть текстове повiдомлення.")
        return ADDRESS

async def get_pet_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message and update.message.text:
        context.user_data['pet_info'] = update.message.text
        await update.message.reply_text("Введіть сушену продукцію (вага, позиція, ціна):")
        return DRIED_PRODUCTS
    else:
        await update.message.reply_text("Будь ласка, введіть текстове повiдомлення.")
        return PET_INFO

async def get_dried_products(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message and update.message.text:
        context.user_data['dried_products'] = update.message.text
        await update.message.reply_text("Введіть пастилу (вага, позиція, ціна):")
        return PASTILA
    else:
        await update.message.reply_text("Будь ласка, введіть текстове повiдомлення.")
        return DRIED_PRODUCTS

async def get_pastila(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message and update.message.text:
        context.user_data['pastila'] = update.message.text
        await update.message.reply_text("Введіть печиво (вага, позиція, ціна):")
        return COOKIES
    else:
        await update.message.reply_text("Будь ласка, введіть ттекстове повiдомлення.")
        return PASTILA

async def get_cookies(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message and update.message.text:
        context.user_data['cookies'] = update.message.text
        await update.message.reply_text("Введіть іншу продукцію (шт/уп, позиція, ціна):")
        return OTHER_PRODUCTS
    else:
        await update.message.reply_text("Будь ласка, введіть текстове повiдомлення.")
        return COOKIES

async def get_other_products(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message and update.message.text:
        context.user_data['other_products'] = update.message.text
        await update.message.reply_text("Введіть подарунок при наявності:")
        return GIFT
    else:
        await update.message.reply_text("Будь ласка, введіть текстове повiдомлення.")
        return OTHER_PRODUCTS

async def get_gift(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message and update.message.text:
        context.user_data['gift'] = update.message.text
        await update.message.reply_text("Введіть бажане пакування (вид пакування):")
        return PACKAGING
    else:
        await update.message.reply_text("Будь ласка, введіть текстове повiдомлення.")
        return GIFT

async def get_packaging(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message and update.message.text:
        context.user_data['packaging'] = update.message.text
        
        # Отправка данных в канал
        order_message = (
            f"Новий заказ!\n\n"
            f"ПІБ: {context.user_data['name']}\n"
            f"Телефон: {context.user_data['phone']}\n"
            f"Адреса: {context.user_data['address']}\n"
            f"Інформація про улюбленця: {context.user_data['pet_info']}\n"
            f"Сушена продукція: {context.user_data['dried_products']}\n"
            f"Пастила: {context.user_data['pastila']}\n"
            f"Печиво: {context.user_data['cookies']}\n"
            f"Інша продукція: {context.user_data['other_products']}\n"
            f"Подарунок: {context.user_data['gift']}\n"
            f"Пакування: {context.user_data['packaging']}"
        )
        
        await context.bot.send_message(chat_id=CHANNEL_ID, text=order_message)
        await update.message.reply_text("Ваше замовлення відправлено! Дякуємо!")
        return ConversationHandler.END
    else:
        await update.message.reply_text("Будь ласка, введіть текстовое сообщение.")
        return PACKAGING

if __name__ == '__main__':
    app = ApplicationBuilder().token('7466178854:AAFkffo0rR4tRNbylZEKame1KxPL626sKqg').build()

    # Настройте ConversationHandler
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_client_name)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_client_phone)],
            ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_client_address)],
            PET_INFO: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_pet_info)],
            DRIED_PRODUCTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_dried_products)],
            PASTILA: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_pastila)],
            COOKIES: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_cookies)],
            OTHER_PRODUCTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_other_products)],
            GIFT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_gift)],
            PACKAGING: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_packaging)],
        },
        fallbacks=[],
    )

    app.add_handler(conversation_handler)

    app.run_polling()