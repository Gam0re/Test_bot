import asyncio

from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart

token_api = "6626161631:AAH9Nro2O1J2SYb8mIUsX67WG2QviCDyAS4"

bot = Bot(token=token_api)
dp = Dispatcher()

keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Да'), KeyboardButton(text='Нет')]
],
    resize_keyboard=True)

class reg(StatesGroup):
    name = State()
    number = State()
    comment = State()
    TheEnd = State()

@dp.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    await state.set_state(reg.name)
    await message.answer(f"{message.from_user.first_name}, Добро пожаловать в компанию DamnIT")
    await message.answer("Напишите свое ФИО")

@dp.message((lambda message: not message.text.isdigit() and len(message.text) > 6) and reg.name)
async def get_full_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(reg.number)
    await message.answer("Укажите Ваш номер телефона (в формате 7 999 999 99 99)")


@dp.message(lambda message: message.text.replace(" ", "").isdigit() and len(message.text.replace(" ", "")) == 11 and reg.number)
async def get_phone_number(message: types.Message, state: FSMContext):
    await state.update_data(number=message.text)
    await state.set_state(reg.comment)
    await message.answer("Напишите любой комментарий")

@dp.message(reg.comment)
async def confirm_terms(message: types.Message, state: FSMContext):
    await state.update_data(comment=message.text)
    await state.set_state(reg.TheEnd)
    await message.answer("Последний шаг! Ознакомься с вводными положениями")
    await message.answer_document(document=types.FSInputFile(path='D:/test.pdf'))
    await message.answer("Ознакомился ?", reply_markup=keyboard)

@dp.message(reg.TheEnd)
async def confirm_terms(message: types.Message, state: FSMContext):
    if message.text == 'Да':
        await message.answer("Спасибо за успешную регистрацию")
        await message.answer_photo(photo=types.FSInputFile(path='D:/tree.jfif'))
        data = await state.get_data()
        id = 773320368
        await bot.send_message(chat_id=id, text=f'ФИО: {data["name"]}\nТелефон: {data["number"]}\nКомментарий: {data["comment"]}\n')
        await state.clear()
    else:
        await message.answer("Ничего страшного, можешь попробоватьс снова!")
        await state.set_state(reg.comment)


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
