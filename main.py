from aiogram import Bot, Dispatcher, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from aiogram.filters import CommandStart
import os
import dotenv

dotenv.load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot=bot)

support_button = InlineKeyboardButton(
    text="Написать в поддержку",
    url="https://t.me/MuzzyExtrePC"
    )

big_button_1 = InlineKeyboardButton(
    text='Профиль 👤',
    callback_data='profile_button_pressed'
)

big_button_2 = InlineKeyboardButton(
    text='Заказы ✅',
    callback_data='orders_button_pressed'
)

big_button_3 = InlineKeyboardButton(
    text='Поддержка 📞',
    callback_data='support_button_pressed'
)
back_button = InlineKeyboardButton(text="Назад", callback_data="back_to_menu")
back_keyboard = InlineKeyboardMarkup(inline_keyboard=[[back_button]])
support_back_keyboard = InlineKeyboardMarkup(inline_keyboard=[[support_button],
                                                               [back_button]])

# Создаем объект инлайн-клавиатуры
keyboard = InlineKeyboardMarkup(inline_keyboard=[[big_button_1], [big_button_2], [big_button_3]])


@dp.message(CommandStart())
async def process_start_command(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or 'Неизвестный'
    await message.answer(
        text='Бро это твое меню!',
        reply_markup=keyboard
    )
    if user_id != ADMIN_ID:
        await bot.send_message(ADMIN_ID, f"Пользователь {username} ({user_id}) начал использование бота")

@dp.callback_query(lambda query: query.data == 'profile_button_pressed')
async def process_button_1_press(callback: CallbackQuery):
    user_id = callback.from_user.id
    username = callback.from_user.username or 'Неизвестный'
    await callback.message.edit_text(
        text='💼Ваш профиль\n'
             '➖➖➖➖➖➖➖\n'
             f'🆔: {user_id}\n'
             f'👤Имя: {username}\n'
             '✅Заказы: 0\n',
        reply_markup=back_keyboard
    )


@dp.callback_query(lambda query: query.data == 'support_button_pressed')
async def process_button_3_press(callback: CallbackQuery):
    await callback.message.edit_text(
        text='☎️ Нажмите кнопку ниже для связи с Администратором.',
        reply_markup=support_back_keyboard
    )
@dp.callback_query(lambda query: query.data == 'back_to_menu')
async def process_back_button(callback_query: CallbackQuery):
    await callback_query.message.edit_text("Вы вернулись в меню.", reply_markup=keyboard)



if __name__ == '__main__':
    dp.run_polling(bot)