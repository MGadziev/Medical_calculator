from db_act import get_patients_info
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import Message, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from states import BeforeOperationFlow
from db_act import get_patients_info_by_id, update_patient_by_id
import message_texts, buttons
async def get_patients_bo(message: Message,  state: FSMContext):
    await state.clear()
    patients = await get_patients_info(message.from_user.id, status='new')
    if patients:
        builder = ReplyKeyboardBuilder()
        for patient in patients:
            builder.add(KeyboardButton(text=f"{str(patient.id)}:"
                                            f"{str(patient.name)}:{str(patient.card_number)}"))
        builder.adjust(2)
        await message.answer(message_texts.holicestit_stop_list, parse_mode='Markdown')
        await message.answer("Выберите пациента:", reply_markup=builder.as_markup(resize_keyboard=True), )
        await state.set_state(BeforeOperationFlow.SHOW_PATIENT)
        return None
    else:
        await message.answer("Нет новых пациентов", reply_markup=buttons.initial_keyboard_markup)
        return None

async def show_patient_info_bo(message: Message,  state: FSMContext):
    chosen_patient_id = message.text.split(":")[0].strip()
    await state.update_data(chosen_patient_id=chosen_patient_id)
    patient = await get_patients_info_by_id(chosen_patient_id)
    await message.answer(f'Имя: {patient.name}\n'
                         f'Номер карты: {patient.card_number}\n'
                         f'Статус: {patient.status}\n\n'
                         f'Заполните опросник по пациенту', reply_markup=ReplyKeyboardRemove())
    await message.answer(message_texts.holicestit_organization_level, reply_markup=buttons.holicestit_organization_level_markup)
    await state.set_state(BeforeOperationFlow.STEP_1)
    return None

async def holecystit_before_operation_1_bo(message: Message, state: FSMContext):
    await state.update_data(holicestit_organization_level_answer=message.text)
    await message.answer(message_texts.before_operation, parse_mode='Markdown')
    await message.answer(message_texts.age_more_than_55, reply_markup=buttons.yes_no_markup)
    await state.set_state(BeforeOperationFlow.STEP_2)

async def holecystit_before_operation_2_bo(message: Message, state: FSMContext):
    await state.update_data(age_more_than_55_answer=message.text)
    await message.answer(message_texts.imt_more_than_30, reply_markup=buttons.yes_no_markup)
    await state.set_state(BeforeOperationFlow.STEP_3)

async def holecystit_before_operation_3_bo(message: Message, state: FSMContext):
    await state.update_data(imt_more_than_30_answer=message.text)
    await message.answer(message_texts.stoma_operations, reply_markup=buttons.yes_no_markup)
    await state.set_state(BeforeOperationFlow.STEP_4)

async def holecystit_before_operation_4_bo(message: Message, state: FSMContext):
    await state.update_data(stoma_operations_answer=message.text)
    await message.answer(message_texts.jaundice, reply_markup=buttons.yes_no_markup)
    await state.set_state(BeforeOperationFlow.STEP_5)


async def holecystit_before_operation_5_bo(message: Message, state: FSMContext):
    global total_score
    age_weight = 0
    imt_weight = 0
    stoma_operations_weight = 0
    jaundice_weight = 0
    context_data = await state.get_data()
    chosen_patient_id = context_data.get('chosen_patient_id')
    holicestit_organization_level_answer = context_data.get('holicestit_organization_level_answer')
    age_more_than_55_answer = context_data.get('age_more_than_55_answer')
    imt_more_than_30_answer = context_data.get('imt_more_than_30_answer')
    stoma_operations_answer = context_data.get('stoma_operations_answer')
    if age_more_than_55_answer == 'Да':
        age_weight = 1
        age_more_than_55_answer = True
    else:
        age_more_than_55_answer = False
    if imt_more_than_30_answer == 'Да':
        imt_weight = 2
        imt_more_than_30_answer = True
    else:
        imt_more_than_30_answer = False
    if stoma_operations_answer == 'Да':
        stoma_operations_weight = 1
        stoma_operations_answer = True
    else:
        stoma_operations_answer = False
    if message.text == 'Да':
        jaundice_weight = 3
        jaundice_answer = True
    else:
        jaundice_answer = False

    total_score = age_weight + imt_weight + stoma_operations_weight + jaundice_weight
    if holicestit_organization_level_answer == 'Поликлинический уровень':
        # Для поликлинического уровня закрываем доступ во флоу с Интраоперационными факторами риска при помощи статуса "closed"
        await update_patient_by_id(chosen_patient_id, age_more_than_55=age_more_than_55_answer,
                                   holicestit_organization_level=holicestit_organization_level_answer,
                                   imt_more_than_30=imt_more_than_30_answer, stoma_operations=stoma_operations_answer,
                                   jaundice=jaundice_answer, new_status='closed', total_score=total_score)
        if total_score>= 4:
            await message.answer(message_texts.hard_lhe_policlinic_level, reply_markup=buttons.menu_markup, parse_mode='Markdown')
            return None
        else:
            await message.answer(message_texts.easy_lhe_policlinic_level, reply_markup=buttons.menu_markup, parse_mode='Markdown')
            return None

    await update_patient_by_id(chosen_patient_id, age_more_than_55=age_more_than_55_answer, holicestit_organization_level=holicestit_organization_level_answer,
                               imt_more_than_30=imt_more_than_30_answer, stoma_operations=stoma_operations_answer,
                               jaundice=jaundice_answer, new_status='pending_operation', total_score=total_score)

    if holicestit_organization_level_answer == 'Медицинская организация II уровня':
        if total_score>=4:
            await message.answer(message_texts.hard_second_level_organization, reply_markup=buttons.menu_markup, parse_mode='Markdown')
            return None
        else:
            await message.answer(message_texts.easy_second_level_organization, reply_markup=buttons.menu_markup, parse_mode='Markdown')
            return None

    if holicestit_organization_level_answer == 'Окружной стационар II уровня':
        if total_score>=4:
            await message.answer(message_texts.hard_second_level_stacionar, reply_markup=buttons.menu_markup, parse_mode='Markdown')
            return None
        else:
            await message.answer(message_texts.easy_second_level_stacionar, reply_markup=buttons.menu_markup, parse_mode='Markdown')
            return None

    if holicestit_organization_level_answer == 'Медицинская организация III уровня':
        if total_score>=4:
            await message.answer(message_texts.hard_third_level_organization, reply_markup=buttons.menu_markup, parse_mode='Markdown')
            await state.set_state(BeforeOperationFlow.SCHEMAS)
            return None
        else:
            await message.answer(message_texts.easy_third_level_organization, reply_markup=buttons.menu_markup, parse_mode='Markdown')
            return None

