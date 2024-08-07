import message_texts
from aiogram.types import Message, FSInputFile, KeyboardButton
from db_act import create_user, check_user
from aiogram.fsm.context import FSMContext
from states import UserInfo
from buttons import initial_keyboard_markup, faq_buttons, tech_support_buttons


async def get_start(message: Message, state: FSMContext):
    await state.clear()
    if await check_user(message.from_user.id):
        fedorov_photo = FSInputFile('fedorov.png')
        await message.answer_photo(fedorov_photo, caption=message_texts.welcome_msg_text, reply_markup=initial_keyboard_markup, parse_mode='Markdown')
    else:
        await message.answer('Введите свое ФИО')
        await state.set_state(UserInfo.GET_NAME)
        return None

# Флоу регистрации
async def get_name(message: Message, state: FSMContext):
    await message.answer('Введите в какой клинике вы работаете')
    await state.update_data(name=message.text)
    await state.set_state(UserInfo.GET_CLINIC)
    return None

async def get_clinic(message: Message, state: FSMContext):
    context_data = await state.get_data()
    name = context_data.get('name')
    await create_user(message.from_user.id, message.from_user.username, name, message.text)
    await message.answer('Вы успешно зарегистрированы, выберите действие', reply_markup=initial_keyboard_markup)
    return None

# О нас
async def about_us(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(message_texts.about_us_text)
    return None

# FAQ
async def get_faq(message: Message,  state: FSMContext):
    await state.clear()
    await message.answer(message_texts.faq_text, reply_markup=faq_buttons)
    return None

# Техническая поддержка
async def get_support(message: Message,  state: FSMContext):
    await state.clear()
    await message.answer(message_texts.tech_support_text, reply_markup=tech_support_buttons)
    return None
