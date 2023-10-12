import logging
import sqlite3
from datetime import datetime
from aiogram import Bot, types, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ContentTypes
from pycbrf import ExchangeRates
import re

from mywallet.keyboardsfinance import kbstart, kbadvice, kbwallet, kbmul, kbback, kbvid
from config import tokenwall, paytoken

storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)
bot = Bot(token=tokenwall, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)

def compinterest(a):
    n = int(a[0])
    m = int(a[1])
    c = int(a[2])
    b = int(a[3])
    for i in range(n):
        m = m * (1 + b/100)
        m += c * 12
    return round(m, 2)



class Expenses(StatesGroup):
    summ_source = State()

class Income(StatesGroup):
    summ_income = State()

class Goals(StatesGroup):
    goal_name = State()

class MyGoal(StatesGroup):
    goal_add = State()

class CompInt(StatesGroup):
    add_sum = State()

class Suggest(StatesGroup):
    sug_sum = State()

class Subscribe(StatesGroup):
    subs = State()

class CheckOps(StatesGroup):
    output = State()

@dp.message_handler(commands='start')
async def start(message: types.Message):
    id1 = int(message.from_user.id)
    conn = sqlite3.connect('final1db.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS expenses1(id INTEGER, expenses INTEGER, source, date)")
    cursor.execute("CREATE TABLE IF NOT EXISTS income1(id INTEGER, income INTEGER, source, date)")
    cursor.execute("CREATE TABLE IF NOT EXISTS goals(id INTEGER UNIQUE, summ INTEGER, goal, current)")
    cursor.execute("CREATE TABLE IF NOT EXISTS subscribers(id)")
    user = cursor.execute(f"SELECT id FROM expenses1 WHERE id = {id1}").fetchone()
    if not user:
        data = [id1, 0, None, None]
        cursor.execute("INSERT OR IGNORE INTO expenses1 VALUES(?, ?, ?, ?)", data)
        cursor.execute("INSERT OR IGNORE INTO income1 VALUES(?, ?, ?, ?)", data)
        conn.commit()
    await message.answer(f'Привет, {message.from_user.first_name}! Я цифровой финансовый помощник для подростков MyWallet. У меня есть множество функций, какой именно вы хотите воспользоваться?',
                         reply_markup=kbstart)

@dp.message_handler(text=["📈 Добавить доход", "/income"], state=None)
async def addinc(message: types.Message):
    await Income.summ_income.set()
    await message.answer("Введите сумму и источник дохода")

@dp.message_handler(lambda message: not bool(re.search('^[0-9]', message.text)), state=Income.summ_income)
async def suminc(message:types.Message):
    await message.answer("Введите сумму и источник дохода")

@dp.message_handler(lambda message: message.text, state=Income.summ_income)
async def suminc(message:types.Message):
    conn = sqlite3.connect('final1db.db')
    cursor = conn.cursor()
    id1 = int(message.from_user.id)
    s = message.text.split()
    date1 = message.date.strftime("%d.%m")
    if len(s) == 2:
        exp = s[0]
        source = str(s[-1])
        data = [id1, exp, source, date1]
        cursor.execute("INSERT OR IGNORE INTO income1 VALUES(?, ?, ?, ?)", data)
        conn.commit()
        await message.answer("Операция выполнена ✅")
    elif len(s) == 1:
        exp = s[0]
        data = [id1, exp, None, date1]
        cursor.execute("INSERT OR IGNORE INTO income1 VALUES(?, ?, ?, ?)", data)
        conn.commit()
        await message.answer("Операция выполнена ✅")
    elif len(s) > 2:
        exp = s[0]
        source = str(" ".join(s[1::]))
        data = [id1, exp, source, date1]
        cursor.execute("INSERT OR IGNORE INTO income1 VALUES(?, ?, ?, ?)", data)
        conn.commit()
        await message.answer("Операция выполнена ✅")
    await Income.next()

@dp.message_handler(text=["📉 Добавить расход", "/expenses"], state=None)
async def addexp(message:types.Message):
    await Expenses.summ_source.set()
    await message.answer('Введите сумму и источник расхода')

@dp.message_handler(lambda message: not bool(re.search('^[0-9]', message.text)), state=Expenses.summ_source)
async def sumexp(message:types.Message):
    await message.answer("Введите сумму и источник расхода")

@dp.message_handler(lambda message: message.text, state=Expenses.summ_source)
async def sumexp(message:types.Message):
    conn = sqlite3.connect('final1db.db')
    cursor = conn.cursor()
    id1 = int(message.from_user.id)
    s = message.text.split()
    date1 = message.date.strftime("%d.%m")
    if len(s) == 2:
        exp = s[0]
        source = str(s[-1])
        data = [id1, exp, source, date1]
        cursor.execute("INSERT OR IGNORE INTO expenses1 VALUES(?, ?, ?, ?)", data)
        conn.commit()
        await message.answer("Операция выполнена ✅")
    elif len(s) == 1:
        exp = s[0]
        data = [id1, exp, None, date1]
        cursor.execute("INSERT OR IGNORE INTO expenses1 VALUES(?, ?, ?, ?)", data)
        conn.commit()
        await message.answer("Операция выполнена ✅")
    elif len(s) > 2:
        exp = s[0]
        source = str(" ".join(s[1::]))
        data = [id1, exp, source, date1]
        cursor.execute("INSERT OR IGNORE INTO expenses1 VALUES(?, ?, ?, ?)", data)
        conn.commit()
        await message.answer("Операция выполнена ✅")
    await Expenses.next()


@dp.message_handler(text=['💡 Советы', '/advice', '🔙 Назад к советам'])
async def advice(message: types.Message):
    conn = sqlite3.connect('final1db.db')
    cursor = conn.cursor()
    id1 = message.from_user.id
    user = cursor.execute(f"SELECT * FROM subscribers WHERE id = {id1}").fetchone()
    if user:
        await message.answer(
            'Наша команда предлагает вам лучшие советы по финансовой грамотности. Ознакомившись с ними, вы сможете улучшить свои навыки в этой сфере!',
            reply_markup=kbadvice)
    else:
        await message.answer("Этот раздел доступен только по подписке. Оформить её можно с помощью команды /subscription")


@dp.message_handler(text=['💰 Мой кошелек', '/wallet'])
async def wallet(message: types.Message):
    await message.answer('Выберите операцию', reply_markup=kbwallet)


@dp.message_handler(text=['📚 Лучшие книги по финансам', '/books'])
async def books(message:types.Message):
    conn = sqlite3.connect('final1db.db')
    cursor = conn.cursor()
    id1 = message.from_user.id
    user = cursor.execute(f"SELECT * FROM subscribers WHERE id = {id1}").fetchone()
    if user:
        await message.answer(
            "1. <b>Джордж Клейсон, «Самый богатый человек в Вавилоне».</b>\n\n2. <b>Роберт Кийосаки, «Богатый папа, бедный папа».</b>\n\n3. <b>Бодо Шефер, «Путь к финансовой свободе».</b>\n\n4. <b>Наполеон Хилл, «Думай и богатей».</b>\n\n5. <b>Роберт Кийосаки «Квадрант денежного потока».</b>",
            reply_markup=kbback)
    else:
        await message.answer("Этот раздел доступен только по подписке. Оформить её можно с помощью команды /subscription")

@dp.message_handler(text=["📺 Полезные видео по финансам", '/videos'])
async def video(message: types.Message):
    conn = sqlite3.connect('final1db.db')
    cursor = conn.cursor()
    id1 = message.from_user.id
    user = cursor.execute(f"SELECT * FROM subscribers WHERE id = {id1}").fetchone()
    if user:
        await message.answer(
            "1. <b>4 Правила Абсолютной Финансовой Грамотности</b>\n\n2. <b>Как Стать Финансово Грамотным?</b>\n\n3. <b>Финансовая Грамотность за 6 Минут</b>\n\n4. <b>Финансовая Грамотность: Контроль Финансов и Ведение Бюджета</b>\n\n5. <b>11 Финансовых Привычек, Которые Сделали Меня Миллионером</b>",
            reply_markup=kbvid)
    else:
        await message.answer("Этот раздел доступен только по подписке. Оформить её можно с помощью команды /subscription")

@dp.message_handler(text=['📄 Создание стартого капитала'])
async def fmoney(message: types.Message):
    conn = sqlite3.connect('final1db.db')
    cursor = conn.cursor()
    id1 = message.from_user.id
    user = cursor.execute(f"SELECT * FROM subscribers WHERE id = {id1}").fetchone()
    if user:
        await message.answer(
            "1. Закрыть долги при наличии\n\n2. Начать вести учет доходов и расходов. Это можно сделать в нашем боте, напиши /wallet\n\n3. Сформировать подушку безопасности. Это должны быть сбережения на сумму расходов от 3 до 6 месяцев\n\n4. Определиться с целью инвестирования, например накопить на отдых",
            reply_markup=kbback)
    else:
        await message.answer("Этот раздел доступен только по подписке. Оформить её можно с помощью команды /subscription")

@dp.message_handler(text=['📊 Приумножение капитала'])
async def multiply(message: types.Message):
    conn = sqlite3.connect('final1db.db')
    cursor = conn.cursor()
    id1 = message.from_user.id
    user = cursor.execute(f"SELECT * FROM subscribers WHERE id = {id1}").fetchone()
    if user:
        await message.answer(
            "1. <b>Накопительный счёт</b>\n2. <b>Депозит</b>\n3. <b>Недвижимость для сдачи в аренду</b>\n4. <b>Акции</b>\n5. <b>Облигации федерального займа</b>\n6. <b>Индивидуальный инвестиционный счёт</b>\n7. <b>ETF-фонды</b>",
            reply_markup=kbmul)
    else:
        await message.answer("Этот раздел доступен только по подписке. Оформить её можно с помощью команды /subscription")

@dp.callback_query_handler(text='1')
async def q(cb: types.Message):
    await bot.send_message(cb.from_user.id,
                           "Вы переводите деньги на бессрочный счёт, а банк ежемесячно начисляет вам на них процент, пока вы пользуетесь его услугами. При этом ограничений на движение средств нет. Но и процент обычно невысокий.\n\n<b>Срок получения прибыли:</b> от одного месяца.\n\n<b>Риски:</b> практически никаких, если обращаться в проверенный банк и не давать данных доступа к онлайн-банкингу посторонним.",
                           reply_markup=kbback)


@dp.callback_query_handler(text='2')
async def q(cb: types.Message):
    await bot.send_message(cb.from_user.id,
                           "Вы кладёте деньги в банк на фиксированный период и получаете за это проценты. Обратите внимание на соотношение сроков и процентов при плавающей ставке по депозиту. Иногда бывает, что, например, на год положить деньги в банк выгоднее, чем на полгода, но менее выгодно, чем на полтора.\n\nДоходы от депозита в зависимости от условий договора можно обналичивать ежемесячно или приплюсовывать к основной сумме, чтобы потом получить все деньги одновременно. Обратите внимание на наличие капитализации: в этом случае проценты прибавляются к основной сумме ежемесячно, и затем на них тоже начисляются проценты.\n\n<b>Срок получения прибыли:</b> от одного месяца, но выгоднее выбирать более продолжительный период.\n\n<b>Риски:</b> практически никаких, если обращаться в проверенный банк и не давать данных доступа к онлайн-банкингу посторонним.",
                           reply_markup=kbback)


@dp.callback_query_handler(text='3')
async def q(cb: types.Message):
    await bot.send_message(cb.from_user.id,
                           "Будьте готовы к тому, что это очень долгосрочная инвестиция. Покупаете квартиру за 2 миллиона и при арендном платеже без коммунальных услуг в 20 тысяч рублей возвращаете накопления только через 8 лет.\n\nНо при этом у вас в собственности есть квартира. Правда, данные Росстата говорят, что в последние три года снижается стоимость всех типов квартир за исключением элитных. До этого недвижимость стабильно росла в цене.\n\n<b>Срок получения прибыли:</b> первые деньги — через месяц, окупаемость — через несколько лет, но у вас будет квартира, которую можно продать.\n\n<b>Риски:</b> ниже среднего, если тщательно выбирать объект недвижимости и проверять арендаторов.",
                           reply_markup=kbback)


@dp.callback_query_handler(text='4')
async def q(cb: types.Message):
    await bot.send_message(cb.from_user.id,
                           "При инвестировании в акции есть смысл не складывать все яйца в одну корзину и приобрести ценные бумаги нескольких компаний. Это даёт возможность хотя бы сохранить накопления, если стоимость части ценных бумаг резко пойдёт вниз.\n\nПри выборе брокера, который будет представлять вас на бирже, проверьте наличие у него государственной лицензии от Центробанка (до 2013 года — от Федеральной службы по финансовым рынкам), а у его компании — регистрации в России.\n\n<b>Срок получения прибыли:</b> через год — по дивидендам, в любое время — после продажи.\n\n<b>Риски:</b> высокие, если не разобраться в вопросе.",
                           reply_markup=kbback)


@dp.callback_query_handler(text='5')
async def q(cb: types.Message):
    await bot.send_message(cb.from_user.id,
                           "Облигации — долговой инструмент с фиксированной доходностью. В случае с облигациями федерального займа (ОФЗ) государство берёт у вас взаймы, затем возвращает вложенные деньги и благодарит вас процентами. Рыночные ОФЗ можно приобрести у брокера. Их срок и доходность различаются, поэтому подробности надо уточнять для каждого выпуска облигаций конкретно.\n\nВ 2017 году Минфин выпустил«народные» облигации, купить которые можно в ВТБ и Сбербанке, но и продать можно только им же. Доходность заявлена на уровне в 8,5% годовых в среднем за 3 года. По трёхлетним депозитам средневзвешенная ставка составляет 4,85%.\n\n<b>Срок получения прибыли:</b> в зависимости от срока облигации.\n\n<b>Риски:</b> практически никаких, если вы не ждёте банкротства государства.",
                           reply_markup=kbback)


@dp.callback_query_handler(text='6')
async def q(cb: types.Message):
    await bot.send_message(cb.from_user.id,
                           "Индивидуальные инвестиционные счета (ИИС) были введены в 2015 году как инструмент для привлечения россиян к долгосрочному инвестированию в ценные бумаги. Вы зачисляете на него деньги обязательно в рублях, но не более миллиона в год, и можете вкладываться в акции и облигации.\n\nС ними всё понятно, но ИИС позволяет получать доход, даже если просто хранить на нём деньги без движения. Вы можете оформить налоговый вычет до 52 тысяч рублей ежегодно.\n\n<b>Сроки получения прибыли:</b> от трёх лет; если забрать деньги раньше, налоговый вычет придётся вернуть.\n\n<b>Риски:</b> выше, чем у депозита, при достаточно низкой доходности, так как инвестиционный счёт не страхуется Агентством по страхованию вкладов.",
                           reply_markup=kbback)


@dp.callback_query_handler(text='7')
async def q(cb: types.Message):
    await bot.send_message(cb.from_user.id,
                           "Вкладывая деньги в биржевой фонд, вы приобретаете долю принадлежащего ему набора акций разных компаний. Это вполне соответствует требованию о разных корзинах, но облегчает задачу инвестору, так как вам предлагают уже сформированный пакет.\n\nЧем больше компаний в портфеле ETF-фонда, тем больше шансов, что вложения будут приносить хотя бы небольшой, но стабильный доход.\n\n<b>Срок получения прибыли:</b> в зависимости от политики фонда.\n\n<b>Риски:</b> чем больше портфель, тем меньше риски.")



@dp.message_handler(text=['💳 Баланс', '/balance'])
async def balance(message: types.Message):
    id1 = message.from_user.id
    conn = sqlite3.connect('final1db.db')
    cursor = conn.cursor()
    exp1 = str(cursor.execute(f"SELECT SUM(expenses) FROM expenses1 WHERE id = {id1}").fetchall())[2:-3]
    inc1 = str(cursor.execute(f"SELECT SUM(income) FROM income1 WHERE id = {id1}").fetchall())[2:-3]
    if not inc1.isdigit():
        inc1 = '0'
    if not exp1.isdigit():
        exp1 = '0'
    dif = int(inc1) - int(exp1)
    await message.answer(f'Баланс: <b>{dif}</b>\nОбщий доход: <b>{inc1}</b>\nОбщий расход: <b>{exp1}</b>')
    if dif < 0:
        await message.answer("Ваш баланс отрицательный, советуем вам пересмотреть свои расходы, чтобы в следующем месяце исправить своё финансовое положение")


@dp.message_handler(text=['/back', '/menu', '🔙 Назад'])
async def back(message: types.Message):
    await message.answer("Вы попали в главное меню", reply_markup=kbstart)

@dp.message_handler(text=['/mygoal', '🎯 Моя цель'])
async def mygoals(message:types.Message):
    id1 = message.from_user.id
    conn = sqlite3.connect('final1db.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS goals(id INTEGER UNIQUE, summ INTEGER, goal)")
    user = cursor.execute(f"SELECT * FROM goals WHERE id = {id1}").fetchall()
    if user:
        summ = int(str(cursor.execute(f"SELECT summ FROM goals WHERE id = {id1}").fetchone())[1:-2])
        name = str(cursor.execute(f"SELECT goal FROM goals WHERE id = {id1}").fetchone())[2:-3]
        stroka = ''
        cursum = int(str(cursor.execute(f"SELECT current FROM goals WHERE id = {id1}").fetchone())[1:-2])
        if summ <= cursum:
            await message.answer("Вы выполнили свою цель. Поздравляем!🥳")
            await message.answer(f"{'🟩' * 10} 100%")
            await message.answer("Вы можете удалить эту цель с помощью команды /cleargoals и добавить новую с помощью команды /goals.")
        else:
            eq = int((cursum/summ)*100)
            sq_length = eq//10

            if cursum <= 0:
                stroka = "⬜" * 10
            elif sq_length >= 0 and sq_length < 3:
                if int(str(eq)[-1]) >= 1:
                    stroka += '🟥' * (sq_length+1)
                    stroka += "⬜" * (9 - sq_length)
                else:
                    stroka += '🟥' * sq_length
                    stroka += "⬜" * (10-sq_length)

            elif sq_length >= 3 and sq_length < 8:
                if int(str(eq)[-1]) >= 5:
                    stroka += '🟧' * (sq_length+1)
                    stroka += "⬜" * (9 - sq_length)
                else:
                    stroka += '🟧' * sq_length
                    stroka += "⬜" * (10-sq_length)

            elif sq_length >= 8 and sq_length < 10:
                stroka += "🟩" * sq_length
                stroka += "⬜" * (10 - sq_length)

            await message.answer(f"Ваша цель: {name} за {summ} ₽")
            await message.answer(f"Вам осталось накопить: {summ - cursum} ₽")
            await message.answer(f"{stroka} {eq}%")
    else:
        await message.answer("На данный момент у вас нет цели, вы можете добавить её c помощью команды /goals")


@dp.message_handler(text=['addtogoal', '💸 Пополнить баланс цели'], state=None)
async def addtogoal(message:types.Message):
    await MyGoal.goal_add.set()
    await message.answer("Напишите сумму, на которую вы хотите пополнить свою цель")

@dp.message_handler(lambda message:message.text.isdigit(), state=MyGoal.goal_add)
async def addgoal(message:types.Message):
    id1 = message.from_user.id
    summ = message.text
    conn = sqlite3.connect('final1db.db')
    cursor = conn.cursor()
    user = cursor.execute(f"SELECT * FROM goals WHERE id = {id1}").fetchall()
    if user:
        goalname = str(cursor.execute(f"SELECT goal FROM goals WHERE id = {id1}").fetchone())[1:-2]
        date1 = message.date.strftime("%d.%m")
        conn = sqlite3.connect('final1db.db')
        cursor = conn.cursor()
        cursum = int(str(cursor.execute(f"SELECT current FROM goals WHERE id = {id1}").fetchone())[1:-2])
        cursum += int(summ)
        cursor.execute(f"UPDATE goals SET current = {cursum} WHERE id = {id1}")
        data = [id1, summ, f"Пополнение цели {goalname} ", date1]
        cursor.execute("INSERT OR IGNORE INTO expenses1 VALUES(?, ?, ?, ?)", data)
        conn.commit()
        await message.answer(f"Вы пополнили баланс цели '{goalname}' на {summ} ₽")
    else:
        await message.answer(
                "На данный момент у вас нет цели, вы можете добавить её с помощью команды /goals")
    await MyGoal.next()

@dp.message_handler(lambda message: not message.text.isdigit(), state=MyGoal.goal_add)
async def check(message:types.Message):
    await message.answer("Введите число")

@dp.message_handler(commands='allincome')
async def allin(message:types.Message):
    id1 = int(message.from_user.id)
    conn = sqlite3.connect('final1db.db')
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM income1 WHERE income = 0")
    conn.commit()
    pres = cursor.execute(f"SELECT * FROM income1 WHERE id = {id1}").fetchall()
    if pres:
        inc1 = cursor.execute(f"SELECT * FROM income1 WHERE id = {id1}").fetchall()
        for i in range(len(inc1)):
            await message.answer(inc1[i][1::])
    else:
        await message.answer("Вы ещё не добавляли доходы, вы можете добавить их с помощью команды /income")

@dp.message_handler(commands='allexpenses')
async def allex(message:types.Message):
    id1 = int(message.from_user.id)
    conn = sqlite3.connect('final1db.db')
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM expenses1 WHERE expenses = 0")
    conn.commit()
    pres = cursor.execute(f"SELECT * FROM expenses1 WHERE id = {id1}").fetchall()
    if pres:
        exp1 = cursor.execute(f"SELECT * FROM expenses1 WHERE id = {id1}").fetchall()
        for i in range(len(exp1)):
            await message.answer(exp1[i][1::])
    else:
        await message.answer("Вы ещё не добавляли расходы, вы можете добавить их с помощью команды /expenses")

@dp.message_handler(text=['📝 Создать цель', '/goals'], state=None)
async def addgoal(message:types.Message):
    await Goals.goal_name.set()
    await message.answer("Напишите сумму и название цели")

@dp.message_handler(lambda message: not bool(re.search('^[0-9]', message.text)), state=Goals.goal_name)
async def goal(message:types.Message):
    await message.answer("Напишите сумму и название цели")

@dp.message_handler(lambda message:message.text, state=Goals.goal_name)
async def goal(message:types.Message):
    id1 = int(message.from_user.id)
    conn = sqlite3.connect('final1db.db')
    cursor = conn.cursor()
    goalinfo = message.text.split()
    user = cursor.execute(f"SELECT id FROM goals WHERE id = {id1}").fetchone()
    if user:
        await message.answer(
            "У вас уже есть финансовая цель, мы настоятельно рекомендуем достичь её перед преступлением к ещё одной")
    else:
        if not goalinfo:
            await message.answer("Введите число и цель после /goals")
        else:
            if len(goalinfo) == 2:
                summ = goalinfo[0]
                goal = str(goalinfo[-1])
                data = [id1, summ, goal, 0]
                cursor.execute("INSERT OR IGNORE INTO goals VALUES(?, ?, ?, ?)", data)
                conn.commit()
            elif len(goalinfo) == 1:
                summ = goalinfo[0]
                data = [id1, summ, None, 0]
                cursor.execute("INSERT OR IGNORE INTO goals VALUES(?, ?, ?, ?)", data)
                conn.commit()
            elif len(goalinfo) > 2:
                summ = goalinfo[0]
                goal = str(" ".join(goalinfo[1::]))
                data = [id1, summ, goal, 0]
                cursor.execute("INSERT OR IGNORE INTO goals VALUES(?, ?, ?, ?)", data)
                conn.commit()
            await message.answer("Вы  создали финансовую цель, поздравляем!🥳")
    await Goals.next()

@dp.message_handler(commands='cleargoals')
async def clear(message:types.Message):
    id1 = message.from_user.id
    conn = sqlite3.connect('final1db.db')
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM goals WHERE id = {id1}")
    conn.commit()
    await message.answer("Ваша цель была удалена")


@dp.message_handler(commands='help')
async def help(message:types.Message):
    await message.answer("Если у вас возникли какие-либо проблемы, напишите @amirakhmetov, подробно описав вашу проблему")


@dp.message_handler(text=["💵 Курс валют", "/currencies"])
async def message(message: types.Message):
    rates = ExchangeRates(datetime.now())
    await bot.send_photo(chat_id=message.from_user.id, photo="https://yamal-media.ru/images/insecure/rs:fill-down:1080:608/aHR0cHM6Ly8yNTc4/MjQuc2VsY2RuLnJ1/L3lhbWFsbmV3cy9m/NDI1NTVkNi1kNzIu/d2VicA.jpg", caption=f"Курсы валют на сегодняшний день:\n\n\n<b>$</b> Доллар США - <b>{rates['USD'][4]}₽</b>\n<b>€</b> Евро - <b>{rates['EUR'][4]}₽</b>\n<b>¥</b> Японская йена - <b>{rates['JPY'][4]/100}₽</b>\n<b>₣</b> Швейцарский франк - <b>{rates['CHF'][4]}₽</b>\n<b>Kč</b> Чешская крона - <b>{rates['CZK'][4]/10}₽</b>\n<b>₺</b> Турецкая лира - <b>{rates['TRY'][4]/10}₽</b>\n<b>¥</b> Китайский юань - <b>{rates['CNY'][4]}₽</b>\n<b>£</b> Фунт Стерлинга - <b>{rates['GBP'][4]}₽</b>")

@dp.message_handler(text=["/games", "🎲 Настольные игры по финансам"])
async def games(message:types.Message):
    await message.answer("1. <b>Настольная игра «Не в деньгах счастье»</b>\n\n2. <b>Онлайн-викторина «Смешарики в мире финансов»</b>\n\n3. <b>Интеллектуальная онлайн-игра «Первые шаги в мире финансов»</b>\n\n4. <b>Компьютерная квест-игра «Финансовые будни»</b>\n\n5. <b>Деловая игра «Услуги финансовых организаций»</b>\n\n6. <b>Бизнес-симулятор «Доходность и риски»</b>\n\n7. <b>Настольная игра «Монополия»</b>", reply_markup=kbback)

@dp.message_handler(text=['/clearincome', '🗑 Удалить историю доходов'])
async def clearinc(message:types.Message):
    id1 = message.from_user.id
    conn = sqlite3.connect('final1db.db')
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM income1 WHERE id = {id1}")
    conn.commit()
    await message.answer("История ваших доходов была удалена")

@dp.message_handler(text=['/clearexpenses', '🗑 Удалить историю расходов'])
async def clearinc(message:types.Message):
    id1 = message.from_user.id
    conn = sqlite3.connect('final1db.db')
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM expenses1 WHERE id = {id1}")
    conn.commit()
    await message.answer("История ваших расходов была удалена")

@dp.message_handler(commands='compound', state=None)
async def compint(message:types.Message):
    await CompInt.add_sum.set()
    await message.answer("Напишите кол-во лет, стартовый капитал, ежемесячные пополнения и годовую доходность")

@dp.message_handler(lambda message:message.text, state=CompInt.add_sum)
async def addd(message:types.Message):
    comp = message.text.split()
    finalcap = compinterest(comp)
    await message.answer(f"Через {comp[0]} лет у вас будет <b>{finalcap} ₽</b>")
    await CompInt.next()

@dp.message_handler(commands='suggestion', state=None)
async def sug(message:types.Message):
    await Suggest.sug_sum.set()
    await message.answer("Напишите свою зарплату")

@dp.message_handler(lambda message:message.text, state=Suggest.sug_sum)
async def salarylvl(message:types.Message):
    salary = int(message.text)
    await message.answer(f"Отложите:\n\n<b>{salary/5}</b> для инвестиций (если трудно откложить {salary/5}, попробуйте отложить {salary/10})\n\n<b>{salary/2}</b> на необходимые расходы (еда, жилье, проезд)\n\n<b>{salary*0.3}</b> на развлечения и хотелки")
    await Suggest.next()

@dp.message_handler(text=["/subscription", "Оформить подписку"])
async def newsub(message:types.Message):
    await bot.send_invoice(message.from_user.id,
                           title='Подписка My Wallet',
                           description='Эта подписка дает вам доступ ко всем нашим финансовым советам, а также раний доступ к новым функциям',
                           payload=123,
                           provider_token=paytoken,
                           currency='RUB',
                           start_parameter='test_bot',
                           prices=[types.LabeledPrice('Руб', 99_00)])

@dp.pre_checkout_query_handler()
async def proccess_pre_checkout_query(query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query_id=query.id, ok=True)


@dp.message_handler(content_types=ContentTypes.SUCCESSFUL_PAYMENT)
async def subsc(message:types.SuccessfulPayment):
    id1 = message.from_user.id
    await bot.send_message(chat_id=message.from_user.id, text="Вы купили подписку, поздравляю!")
    conn = sqlite3.connect('final1db.db')
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO subscribers VALUES(?)", (id1,))
    conn.commit()

@dp.message_handler(text=["Найти операцию", '/findop'])
async def findop(message:types.Message):
    await message.answer('Введите дату, за которую вы хотите найти операцию (в виде dd.mm, например 31.12)')
    await CheckOps.output.set()

@dp.message_handler(commands='cancel', state=CheckOps.output)
async def cancel(message:types.Message):
    await message.answer("Вы вернулись в главное меню", reply_markup=kbstart)
    await CheckOps.next()

# @dp.message_handler(regexp='\d\d\\.\d\d')
@dp.message_handler(lambda message: bool(re.match('\d\d\\.\d\d', message.text)), state=CheckOps.output)
async def check(message:types.Message):
    conn = sqlite3.connect('final1db.db')
    cursor = conn.cursor()
    id1 = message.from_user.id
    text1 = message.text
    exp_op = cursor.execute(f"SELECT * FROM expenses1 WHERE id = {id1} AND date = {text1}").fetchall()
    inc_op = cursor.execute(f"SELECT * FROM income1 WHERE id = {id1} AND date = {text1}").fetchall()
    if len(exp_op) > 0:
        exp_list = ''
        exp_list += '<b>Расходы за выбранный день</b>\n'
        for i in exp_op:
            exp_list += f'{i[1]} ₽ - {i[2]}\n'
        await message.answer(exp_list)
    else:
        await message.answer("<b>У вас нет расходов за выбранный день</b>")

    if len(inc_op) > 0:
        inc_list = ''
        inc_list += '<b>Доходы за выбранный день</b>\n'
        for i in inc_op:
            inc_list += f'{i[1]} ₽ - {i[2]}\n'
        await message.answer(inc_list)
    else:
        await message.answer("<b>У вас нет доходов за выбранный день</b>")
    await CheckOps.next()

@dp.message_handler(lambda message: not bool(re.match('\d\d\\.\d\d', message.text)), state=CheckOps.output)
async def check(message:types.Message):
    await message.answer('Введите дату в формате dd.mm (31.12)')



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
