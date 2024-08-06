import buttons
from db_act import get_patients_info
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import Message, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from states import PatientNote
from db_act import update_patient_by_id


async def get_patients_for_note(message: Message,  state: FSMContext):
    await state.clear()
    patients = await get_patients_info(message.from_user.id)
    builder = ReplyKeyboardBuilder()
    if patients:
        for patient in patients:
            builder.add(KeyboardButton(text=f"{str(patient.id)}:"
                                            f"{str(patient.name)}:{str(patient.card_number)}"))
        builder.adjust(4)
        await message.answer("Выберите пациента:", reply_markup=builder.as_markup(resize_keyboard=True), )
        await state.set_state(PatientNote.ADD_NOTE)
    else:
        await message.answer("У вас нет пациентов", reply_markup=buttons.initial_keyboard_markup )
    return None


async def add_patient_note(message: Message,  state: FSMContext):
    chosen_patient_id = message.text.split(":")[0].strip()
    await state.update_data(chosen_patient_id=chosen_patient_id)
    await state.set_state(PatientNote.SAVE_NOTE)
    await message.answer("Напишите ваш комментарий", reply_markup=ReplyKeyboardRemove() )
    return None


async def save_patient_note(message: Message,  state: FSMContext):
    context_data = await state.get_data()
    chosen_patient_id = context_data.get('chosen_patient_id')
    await update_patient_by_id(chosen_patient_id, comment=message.text)
    await message.answer("Комментарий сохранен", reply_markup=ReplyKeyboardRemove() )
    await state.clear()
    return None