from db_act import get_patients_info
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import Message, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from states import DuringOperationFlow
from db_act import get_patients_info_by_id, update_patient_by_id
import message_texts, buttons

async def get_patients_do(message: Message,  state: FSMContext):
    await state.clear()
    patients = await get_patients_info(message.from_user.id, status='pending_operation')
    if patients:
        builder = ReplyKeyboardBuilder()
        for patient in patients:
            builder.add(KeyboardButton(text=f"{str(patient.id)}:"
                                            f"{str(patient.name)}:{str(patient.card_number)}"))
        builder.adjust(2)
        await message.answer("Выберите пациента:", reply_markup=builder.as_markup(resize_keyboard=True), )
        await state.set_state(DuringOperationFlow.SHOW_PATIENT)
        return None
    else:
        await message.answer("Нет пациентов с заполненными предоперационными факторами", reply_markup=buttons.initial_keyboard_markup)
        return None

async def show_patient_info_do(message: Message,  state: FSMContext):
    chosen_patient_id = message.text.split(":")[0].strip()
    await state.update_data(chosen_patient_id=chosen_patient_id)
    patient = await get_patients_info_by_id(chosen_patient_id)
    await message.answer(f'Имя: {patient.name}\n'
                         f'Номер карты: {patient.card_number}\n'
                         f'Статус: {patient.status}\n'
                         f'Уровень мед.учреждения: {patient.holicestit_organization_level}\n\n'
                         f'Заполните опросник по пациенту', reply_markup=ReplyKeyboardRemove())
    await message.answer(message_texts.adhesion, reply_markup=buttons.yes_no_markup)
    await state.set_state(DuringOperationFlow.STEP_1)
    return None


# Постооперационные факторы
async def holecystit_during_operation_1_do(message: Message, state: FSMContext):
    await state.update_data(adhesion_answer=message.text)
    await message.answer(message_texts.omentum, reply_markup=buttons.yes_no_markup)
    await state.set_state(DuringOperationFlow.STEP_2)

async def holecystit_during_operation_2_do(message: Message, state: FSMContext):
    await state.update_data(omentum_answer=message.text)
    await message.answer(message_texts.fibrose_changes, reply_markup=buttons.yes_no_markup)
    await state.set_state(DuringOperationFlow.STEP_3)

async def holecystit_during_operation_3_do(message: Message, state: FSMContext):
    await state.update_data(fibrose_changes_answer=message.text)
    await message.answer(message_texts.infiltrat, reply_markup=buttons.yes_no_markup)
    await state.set_state(DuringOperationFlow.STEP_4)

async def holecystit_during_operation_4_do(message: Message, state: FSMContext):
    global total_score
    adhesion_weight = 0
    omentum_weight = 0
    fibrose_changes_weight = 0
    infiltrat_weight = 0

    context_data = await state.get_data()
    chosen_patient_id = context_data.get('chosen_patient_id')
    patient = await get_patients_info_by_id(chosen_patient_id)
    adhesion_answer = context_data.get('adhesion_answer')
    omentum_answer = context_data.get('omentum_answer')
    fibrose_changes_answer = context_data.get('fibrose_changes_answer')
    infiltrat_answer = message.text
    if adhesion_answer == 'Да':
        adhesion_weight = 1
        adhesion_answer = True
    else:
        adhesion_answer = False
    if omentum_answer == 'Да':
        omentum_weight = 2
        omentum_answer = True
    else:
        omentum_answer = False
    if fibrose_changes_answer == 'Да':
        fibrose_changes_weight = 4
        fibrose_changes_answer = True
    else:
        fibrose_changes_answer = False
    if infiltrat_answer == 'Да':
        infiltrat_weight = 5
        infiltrat_answer = True
    else:
        infiltrat_answer = False

    total_score = patient.total_score + adhesion_weight+omentum_weight+fibrose_changes_weight+infiltrat_weight
    await update_patient_by_id(chosen_patient_id, adhesion=adhesion_answer, omentum=omentum_answer,
                               fibrose_changes=fibrose_changes_answer, infiltrat=infiltrat_answer, total_score=total_score, new_status='closed')
    if patient.holicestit_organization_level == 'Медицинская организация II уровня':
        if total_score>=4:
            await message.answer(message_texts.hard_second_level_organization_during_operation, reply_markup=ReplyKeyboardRemove(), parse_mode='Markdown')
            return None
        else:
            await message.answer(message_texts.easy_second_level_organization_during_operation, reply_markup=ReplyKeyboardRemove(), parse_mode='Markdown')
            return None

    if patient.holicestit_organization_level == 'Окружной стационар II уровня':
        if total_score>=4:
            await message.answer(message_texts.hard_second_level_stacionar_during_operation, reply_markup=ReplyKeyboardRemove(), parse_mode='Markdown')
            return None
        else:
            await message.answer(message_texts.easy_second_level_stacionar_during_operation, reply_markup=ReplyKeyboardRemove(), parse_mode='Markdown')
            return None

    if patient.holicestit_organization_level == 'Медицинская организация III уровня':
        if total_score>=4:
            await message.answer(message_texts.hard_third_level_organization_during_operation, reply_markup=buttons.schema_keyboard_markup, parse_mode='Markdown')
            await state.set_state(DuringOperationFlow.SCHEMAS)
            return None
        else:
            await message.answer(message_texts.easy_third_level_organization_during_operation, reply_markup=ReplyKeyboardRemove(), parse_mode='Markdown')
            return None
