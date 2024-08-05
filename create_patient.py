from aiogram.types import Message
from db_act import create_patient
from aiogram.fsm.context import FSMContext
from states import CreatePatient
from buttons import initial_keyboard_markup

async def create_patient_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Введите ФИО пациента')
    await state.set_state(CreatePatient.GET_NAME)
    return None

# Флоу регистрации
async def get_patient_name(message: Message, state: FSMContext):
    await state.update_data(patient_name=message.text)
    await message.answer('Введите номер карты пациента')
    await state.set_state(CreatePatient.GET_NUMBER)
    return None

async def get_patient_number(message: Message, state: FSMContext):
    context_data = await state.get_data()
    patient_name = context_data.get('patient_name')
    if await create_patient(patient_name, message.text, message.from_user.id):
        await message.answer('Пациент создан', reply_markup=initial_keyboard_markup)
        await state.clear()
    else:
        await message.answer('Ошибка при создании пациента\n'
                             'Обратитесь в поддержку либо попробуйте снова ', reply_markup=initial_keyboard_markup)
        await state.clear()
    return None