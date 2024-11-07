import asyncio
from settings import *
from aiogram import Dispatcher, Bot, types, F
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


dp = Dispatcher()
bot = Bot(Token, default=DefaultBotProperties(
    parse_mode=ParseMode.HTML))
active_ids = []


# Этот хэндлер будет срабатывать на команду "/start"
@ dp.message(Command('start'))
async def start_command(message: types.Message) -> None:
    kb = [
        [types.InlineKeyboardButton(
            text='Начать приём заявок', callback_data='start_workday')],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    await message.answer('Эскадро саппорт приветствует тебя!', reply_markup=keyboard)


# Этот хэндлер будет срабатывать на кнопку Меню
@ dp.callback_query(F.data == 'menu')
async def menu_callback(callback: types.CallbackQuery):
    kb = [
        [types.InlineKeyboardButton(
            text='Начать приём заявок', callback_data='start_workday')],
        [types.InlineKeyboardButton(
            text='Список заявок', url='https://bitrix24.dltkmsk.ru/rpa/list/2/')],
        # [types.InlineKeyboardButton(
        #    text='Мои заявки', callback_data='my_tickets')],
        [types.InlineKeyboardButton(
            text='Остановить приём заявок', callback_data='end_workday')]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    await callback.message.edit_text('Эскадро саппорт приветствует тебя!', reply_markup=keyboard)


# Этот хэндлер будет срабатывать на кнопку Начать Рабочий День
@ dp.callback_query(F.data == 'start_workday')
async def start_workday_callback(callback: types.CallbackQuery):
    userid = callback.from_user.id
    active_ids.append(userid)
    print(f'''user {userid} added to active_ids. Current active_ids: {
          active_ids}''')
    kb = [
        [types.InlineKeyboardButton(
            text='Список заявок', url='https://bitrix24.dltkmsk.ru/rpa/list/2/')],
        [types.InlineKeyboardButton(
            text='Остановить приём заявок', callback_data='end_workday')],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    await callback.message.edit_text('Отлично, ты в работе!\n'
                                     'Для выбора доступных заявок просмотри открытые и выбери интересующие.', reply_markup=keyboard)


# Кнопка-ссылка на список заявок в битре
@ dp.callback_query(F.data == 'active_tickets')
async def start_workday_callback(callback: types.CallbackQuery):
    kb = [
        [
            types.InlineKeyboardButton(text="Меню", callback_data='menu')
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    await callback.message.edit_text(f'Вот список открытых заявок:'
                                     '', reply_markup=keyboard)


# Этот хэндлер будет срабатывать на кнопку Закончить Рабочий День
@ dp.callback_query(F.data == 'end_workday')
async def start_workday_callback(callback: types.CallbackQuery):
    print(f'chat_id: {callback.from_user.id}')
    userid = callback.from_user.id
    try:
        active_ids.remove(userid)
        print(f'''user {userid} removed from active_ids. Current active_ids: {
              active_ids}''')
    except Exception as e:
        print(e)
    kb = [
        [
            types.InlineKeyboardButton(
                text='Начать приём заявок', callback_data='start_workday')
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    await callback.message.edit_text(f'Спасибо за работу До новых встреч в эфире!', reply_markup=keyboard)


async def send_msg(message):
    print('---------------------function send_msg started...------------------')
    print(f'active_ids: {active_ids}')
    for active_id in active_ids():
        kb = [[types.InlineKeyboardButton(text="Меню", callback_data='menu')],]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)

        try:
            print(f'sending message to id {active_id}...')
            await bot.send_message(chat_id=active_id, text=message, reply_markup=keyboard)
            print(f'message to id {active_id} sent.')
        except Exception as e:
            print(e)


async def escadrobot_main() -> None:
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(escadrobot_main())
