import buttons
from db_act import get_patients_info
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import Message, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from states import ShowPatient
from db_act import get_patients_info_by_id

async def get_patients(message: Message,  state: FSMContext):
    await state.clear()
    patients = await get_patients_info(message.from_user.id)
    builder = ReplyKeyboardBuilder()
    if patients:
        for patient in patients:
            builder.add(KeyboardButton(text=f"{str(patient.id)}:"
                                            f"{str(patient.name)}:{str(patient.card_number)}"))
        builder.adjust(4)
        await message.answer("Выберите пациента:", reply_markup=builder.as_markup(resize_keyboard=True), )
        await state.set_state(ShowPatient.SHOW_PATIENT)
    else:
        await message.answer("У вас нет пациентов", reply_markup=builder.as_markup(resize_keyboard=True), )
    return None

async def show_patient_info(message: Message,  state: FSMContext):
    chosen_patient_id = message.text.split(":")[0].strip()
    patient = await get_patients_info_by_id(chosen_patient_id)
    await message.answer(f'Имя: {patient.name}\n'
                         f'Номер карты: {patient.card_number}\n'
                         f'Статус: {status.get(patient.status)}\n'
                         f'Уровень организации: {patient.holicestit_organization_level}\n\n'
                         '1. Возраст пациента старше 55 лет?\n'
                         '2. ИМТ пациента больше 30 кг/м²?\n'
                         '3. Были ли у пациента операции на органах брюшной полости?\n'
                         '4. Есть ли у пациента механическая желтуха в анамнезе?\n'
                         '5. Есть ли спаечный процесс в верхнем этаже брюшной полости?\n'
                         '6. Есть ли окутанность желчного пузыря фиксированной прядью большого сальника?\n'
                         '7. Есть ли фиброзные изменения желчного пузыря?\n'
                         '8. Есть ли у пациента околопузырный инфильтрат?\n\n')
    await message.answer(
                         '```Критерии\n'
                         '| № |Статус \n'
                         '|---|------\n'
                         f'| 1 | {criteria_dict.get(patient.age_more_than_55)}\n'
                         f'| 2 | {criteria_dict.get(patient.imt_more_than_30)}\n'
                         f'| 3 | {criteria_dict.get(patient.stoma_operations)} \n'
                         f'| 4 | {criteria_dict.get(patient.jaundice)}\n'
                         f'| 5 | {criteria_dict.get(patient.adhesion)}\n'
                         f'| 6 | {criteria_dict.get(patient.omentum)}\n'
                         f'| 7 | {criteria_dict.get(patient.fibrose_changes)}\n'
                         f'| 8 | {criteria_dict.get(patient.infiltrat)}```\n'
                         f'Комментарий: {patient.comment}\n', reply_markup=buttons.menu_markup, parse_mode='Markdown')
    await state.clear()
    return None

criteria_dict = {
    True: "Да",
    False: "Нет",
    None: "Критерий не заполнен"
}

status = {
    'pending_operation': "Ожидает операции",
    'new': "Новый",
    'closed': "Закрыт"
}