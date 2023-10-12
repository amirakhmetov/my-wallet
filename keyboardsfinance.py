from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


kbstart = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton('💰 Мой кошелек')
b2 = KeyboardButton("💵 Курс валют")
b3 = KeyboardButton('💡 Советы')
kbstart.add(b1, b2 ,b3)

kbadvice = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
ad1 = KeyboardButton("📄 Создание стартого капитала")
ad2 = KeyboardButton("📊 Приумножение капитала")
ad3 = KeyboardButton("📚 Лучшие книги по финансам")
ad4 = KeyboardButton("📺 Полезные видео по финансам")
ad5 = KeyboardButton("🎲 Настольные игры по финансам")
ad6 = KeyboardButton("🔙 Назад")
kbadvice.add(ad1, ad2, ad3, ad4, ad5, ad6)

kbwallet = ReplyKeyboardMarkup(resize_keyboard=True)
w1 = KeyboardButton("💳 Баланс")
w2 = KeyboardButton("📉 Добавить расход")
w3 = KeyboardButton("🗑 Удалить историю расходов")
w4 = KeyboardButton("📈 Добавить доход")
w5 = KeyboardButton("🗑 Удалить историю доходов")
w6 = KeyboardButton("📝 Создать цель")
w7 = KeyboardButton("🎯 Моя цель")
w8 = KeyboardButton("💸 Пополнить баланс цели")
w9 = KeyboardButton("🔙 Назад")
kbwallet.add(w1, w2, w3, w4, w5, w6 ,w7, w8, w9)

kbmul = InlineKeyboardMarkup(row_width=4)
mul1 = InlineKeyboardButton("1", callback_data=1)
mul2 = InlineKeyboardButton("2", callback_data=2)
mul3 = InlineKeyboardButton("3", callback_data=3)
mul4 = InlineKeyboardButton("4", callback_data=4)
mul5 = InlineKeyboardButton("5", callback_data=5)
mul6 = InlineKeyboardButton("6", callback_data=6)
mul7 = InlineKeyboardButton("7", callback_data=7)
kbmul.add(mul1, mul2, mul3, mul4, mul5, mul6, mul7)

kbback = ReplyKeyboardMarkup(resize_keyboard=True)
backbtn = KeyboardButton("🔙 Назад к советам")
kbback.add(backbtn)

kbvid = InlineKeyboardMarkup(row_width=1)
vid1 = InlineKeyboardButton("Первое видео", url="https://youtu.be/CkMUsGO12gA", callback_data='vi1')
vid2 = InlineKeyboardButton("Второе видео", url="https://youtu.be/a8kV0zVWRX4",  callback_data='vi2')
vid3 = InlineKeyboardButton("Третье видео", url="https://youtu.be/S88HZWjuVZg", callback_data='vi3')
vid4 = InlineKeyboardButton("Четвертое видео", url="https://youtu.be/TfQALmUyZ1E",  callback_data='vi4')
vid5 = InlineKeyboardButton("Пятое видео", url="https://youtu.be/0KjLq3b1YB8", callback_data='vi5')
kbvid.add(vid1, vid2, vid3, vid4, vid5)

# exchange_kb = ReplyKeyboardMarkup(resize_keyboard=True)
# exchangeButton = KeyboardButton("Узнать текущие курсы валют")
# exchange_kb.add(exchangeButton)
# @dp.message_handler(commands=["currencies"])
# async def start(message: types.Message):
#     await message.answer("Привет здесь ты можешь узнать текущий курс валют", reply_markup=exchange_kb)

