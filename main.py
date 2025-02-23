import telebot as tl
import keyboa
from main1 import schedule
import datetime


token = tl.TeleBot('7889302534:AAGF6EU5sgVU5YItag-PXcsCqX1LXtwIT7E')
f = []
kf = []
schedules = schedule
s = list(schedules.keys())
for i in range(0, len(s)):
    k = {s[i]: 'one:' + s[i]}
    kf.append(k)
days = {0: 'Понедельник', 1: 'Вторник', 2: 'Среду', 3: 'Четверг', 4: 'Пятницу', 5: 'субботу', 6: 'воскресение'}


@token.message_handler(commands=['start'])
def start(sms):
    markup = tl.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = tl.types.KeyboardButton('Расписание')
    markup.row(btn)
    token.send_message(sms.chat.id, text="Привет, {0.first_name}! Я бот, который дает расписание ".format(sms.from_user), reply_markup = markup)


@token.message_handler(content_types=['text'])
def check_text(message):
    if message.text == 'Расписание':
        f.clear()
        kb = keyboa.Keyboa(kf, items_in_row=2).keyboard
        token.send_message(message.chat.id, text="Выберите класс:", reply_markup=kb)
    else:
        token.send_message(message.chat.id, text="Пожалуйста, нажмите конпку <Расписание>.")


@token.callback_query_handler(func=lambda callback:callback.data.startswith('one:'))
def callback_sms_one(callback):
    f.append(callback.data[4:])
    day = datetime.datetime.now().weekday()+1
    if datetime.datetime.now().weekday()+1 == 7:
        day = 0
    markup = tl.types.InlineKeyboardMarkup()
    btn1 = tl.types.InlineKeyboardButton('Расписание на сегодня', callback_data=f'two:{days[datetime.datetime.now().weekday()]}')
    btn2 = tl.types.InlineKeyboardButton('Расписание на завтра', callback_data=f'two:{day}')
    btn3 = tl.types.InlineKeyboardButton('Другое', callback_data='other:Другое')
    markup.row(btn1)
    markup.row(btn2)
    markup.row(btn3)
    token.send_message(callback.message.chat.id, text="Выберите:", reply_markup=markup)
    token.delete_message(callback.message.chat.id, callback.message.message_id)


@token.callback_query_handler(func=lambda callback:callback.data.startswith('other:'))
def callback_sms_other(callback):
    markup = tl.types.InlineKeyboardMarkup()
    btn1 = tl.types.InlineKeyboardButton('понедельник', callback_data='two:Понедельник')
    btn2 = tl.types.InlineKeyboardButton('вторник', callback_data='two:Вторник')
    btn3 = tl.types.InlineKeyboardButton('среда', callback_data='two:Среду')
    btn4 = tl.types.InlineKeyboardButton('четверг', callback_data='two:Четверг')
    btn5 = tl.types.InlineKeyboardButton('пятница', callback_data='two:Пятницу')
    btn6 = tl.types.InlineKeyboardButton('суббота', callback_data='two:субботу')
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)
    markup.row(btn5, btn6)
    token.send_message(callback.message.chat.id, text="Выберите день недели:", reply_markup=markup)
    token.delete_message(callback.message.chat.id, callback.message.message_id)


@token.callback_query_handler(func=lambda callback:callback.data.startswith('two:'))
def callback_sms_two(callback):
    try:
        answer_sms = '\n'
        for lesson in schedules[f[0]][callback.data[4:]]:
            answer_sms += lesson + '\n'
        token.delete_message(callback.message.chat.id, callback.message.message_id)
        token.send_message(callback.message.chat.id, text=f"расписание на {callback.data[4:].lower()} {f[0]} класса:{answer_sms}")

    except:
        markup = tl.types.InlineKeyboardMarkup()
        btn1 = tl.types.InlineKeyboardButton('Назад', callback_data='other:Назад')
        markup.row(btn1)
        token.delete_message(callback.message.chat.id, callback.message.message_id)
        token.send_message(callback.message.chat.id, text=f"Извините, но в {callback.data[4:].lower()} вы не учитесь. Вернитесь назад и выберите другой день недели", reply_markup=markup)


token.polling(none_stop=True, interval=0)