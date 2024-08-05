from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile
from aiogram.fsm.context import FSMContext
import buttons
import message_texts
from states import HolecystitOperation

total_score = 0
# Предоперационные факторы
async def holecystit_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(message_texts.holicestit_stop_list, parse_mode='Markdown')
    await message.answer(message_texts.holicestit_organization_level, reply_markup=buttons.holicestit_organization_level_markup)
    await state.set_state(HolecystitOperation.STEP_1)

async def holecystit_before_operation_1(message: Message, state: FSMContext):
    await state.update_data(holicestit_organization_level_answer=message.text)
    await message.answer(message_texts.before_operation, parse_mode='Markdown')
    await message.answer(message_texts.age_more_than_55, reply_markup=buttons.yes_no_markup)
    await state.set_state(HolecystitOperation.STEP_2)

async def holecystit_before_operation_2(message: Message, state: FSMContext):
    await state.update_data(age_more_than_55_answer=message.text)
    await message.answer(message_texts.imt_more_than_30, reply_markup=buttons.yes_no_markup)
    await state.set_state(HolecystitOperation.STEP_3)

async def holecystit_before_operation_3(message: Message, state: FSMContext):
    await state.update_data(imt_more_than_30_answer=message.text)
    await message.answer(message_texts.stoma_operations, reply_markup=buttons.yes_no_markup)
    await state.set_state(HolecystitOperation.STEP_4)

async def holecystit_before_operation_4(message: Message, state: FSMContext):
    await state.update_data(stoma_operations_answer=message.text)
    await message.answer(message_texts.jaundice, reply_markup=buttons.yes_no_markup)
    await state.set_state(HolecystitOperation.STEP_5)


async def holecystit_before_operation_5(message: Message, state: FSMContext):
    global total_score
    age_weight = 0
    imt_weight = 0
    stoma_operations_weight = 0
    jaundice_weight = 0
    context_data = await state.get_data()
    holicestit_organization_level_answer = context_data.get('holicestit_organization_level_answer')
    age_more_than_55_answer = context_data.get('age_more_than_55_answer')
    imt_more_than_30_answer = context_data.get('imt_more_than_30_answer')
    stoma_operations_answer = context_data.get('stoma_operations_answer')
    if age_more_than_55_answer == 'Да':
        age_weight = 1
    if imt_more_than_30_answer == 'Да':
        imt_weight = 2
    if stoma_operations_answer == 'Да':
        stoma_operations_weight = 1
    if message.text == 'Да':
        jaundice_weight = 3
    total_score = age_weight + imt_weight + stoma_operations_weight + jaundice_weight
    print(total_score)
    if holicestit_organization_level_answer == 'Поликлинический уровень':
        if total_score>= 4:
            await message.answer(message_texts.hard_lhe_policlinic_level, reply_markup=ReplyKeyboardRemove(), parse_mode='Markdown')
            return None
        else:
            await message.answer(message_texts.easy_lhe_policlinic_level, reply_markup=ReplyKeyboardRemove(), parse_mode='Markdown')
            return None

    if holicestit_organization_level_answer == 'Медицинская организация II уровня':
        if total_score>=4:
            await message.answer(message_texts.hard_second_level_organization, reply_markup=ReplyKeyboardRemove(), parse_mode='Markdown')
            return None
        else:
            await message.answer(message_texts.easy_second_level_organization, reply_markup=ReplyKeyboardRemove(), parse_mode='Markdown')
            await message.answer(message_texts.adhesion, reply_markup=buttons.yes_no_markup)
            await message.answer(message_texts.inter_operation, parse_mode='Markdown')
            await state.set_state(HolecystitOperation.STEP_6)
            return None

    if holicestit_organization_level_answer == 'Окружной стационар II уровня':
        if total_score>=4:
            await message.answer(message_texts.hard_second_level_stacionar, reply_markup=ReplyKeyboardRemove(), parse_mode='Markdown')
            return None
        else:
            await message.answer(message_texts.easy_second_level_stacionar, reply_markup=ReplyKeyboardRemove(), parse_mode='Markdown')
            await state.set_state(HolecystitOperation.STEP_6)
            await message.answer(message_texts.inter_operation, parse_mode='Markdown')
            await message.answer(message_texts.adhesion, reply_markup=buttons.yes_no_markup)
            return None

    if holicestit_organization_level_answer == 'Медицинская организация III уровня':
        if total_score>=4:
            await message.answer(message_texts.hard_third_level_organization, reply_markup=buttons.schema_keyboard_markup, parse_mode='Markdown')
            await state.set_state(HolecystitOperation.STEP_10)
            return None
        else:
            await message.answer(message_texts.easy_third_level_organization, reply_markup=ReplyKeyboardRemove(), parse_mode='Markdown')
            await state.set_state(HolecystitOperation.STEP_6)
            await message.answer(message_texts.inter_operation, parse_mode='Markdown')
            await message.answer(message_texts.adhesion, reply_markup=buttons.yes_no_markup)
            return None


# Постооперационные факторы
async def holecystit_during_operation_1(message: Message, state: FSMContext):
    await state.update_data(adhesion_answer=message.text)
    await message.answer(message_texts.omentum, reply_markup=buttons.yes_no_markup)
    await state.set_state(HolecystitOperation.STEP_7)

async def holecystit_during_operation_2(message: Message, state: FSMContext):
    await state.update_data(omentum_answer=message.text)
    await message.answer(message_texts.fibrose_changes, reply_markup=buttons.yes_no_markup)
    await state.set_state(HolecystitOperation.STEP_8)

async def holecystit_during_operation_3(message: Message, state: FSMContext):
    await state.update_data(fibrose_changes_answer=message.text)
    await message.answer(message_texts.infiltrat, reply_markup=buttons.yes_no_markup)
    await state.set_state(HolecystitOperation.STEP_9)

async def holecystit_during_operation_4(message: Message, state: FSMContext):
    global total_score
    adhesion_weight = 0
    omentum_weight = 0
    fibrose_changes_weight = 0
    infiltrat_weight = 0
    context_data = await state.get_data()
    adhesion_answer = context_data.get('adhesion_answer')
    omentum_answer = context_data.get('omentum_answer')
    fibrose_changes_answer = context_data.get('fibrose_changes_answer')
    infiltrat_answer = message.text
    holicestit_organization_level_answer = context_data.get('holicestit_organization_level_answer')

    if adhesion_answer == 'Да':
        adhesion_weight = 1
    if omentum_answer == 'Да':
        omentum_weight = 2
    if fibrose_changes_answer == 'Да':
        fibrose_changes_weight = 4
    if infiltrat_answer == 'Да':
        infiltrat_weight = 5
    total_score = total_score + adhesion_weight+omentum_weight+fibrose_changes_weight+infiltrat_weight
    print(total_score)
    if holicestit_organization_level_answer == 'Медицинская организация II уровня':
        if total_score>=4:
            await message.answer(message_texts.hard_second_level_organization_during_operation, reply_markup=ReplyKeyboardRemove(), parse_mode='Markdown')
            return None
        else:
            await message.answer(message_texts.easy_second_level_organization_during_operation, reply_markup=ReplyKeyboardRemove(), parse_mode='Markdown')
            return None

    if holicestit_organization_level_answer == 'Окружной стационар II уровня':
        if total_score>=4:
            await message.answer(message_texts.hard_second_level_stacionar_during_operation, reply_markup=ReplyKeyboardRemove(), parse_mode='Markdown')
            return None
        else:
            await message.answer(message_texts.easy_second_level_stacionar_during_operation, reply_markup=ReplyKeyboardRemove(), parse_mode='Markdown')
            return None

    if holicestit_organization_level_answer == 'Медицинская организация III уровня':
        if total_score>=4:
            await message.answer(message_texts.hard_third_level_organization_during_operation, reply_markup=buttons.schema_keyboard_markup, parse_mode='Markdown')
            await state.set_state(HolecystitOperation.STEP_10)
            return None
        else:
            await message.answer(message_texts.easy_third_level_organization_during_operation, reply_markup=ReplyKeyboardRemove(), parse_mode='Markdown')
            return None

async def show_schemas(message: Message, state: FSMContext):
    await state.clear()
    if message.text == 'ЖКБ, осложненная холедохолитиазом':
        await message.answer(message_texts.schema_1, reply_markup=ReplyKeyboardRemove(), parse_mode='Markdown')
    if message.text == 'Трудная анатомия':
        await message.answer(message_texts.schema_2, reply_markup=ReplyKeyboardRemove(), parse_mode='Markdown')
    if message.text == 'Сморщенный пузырь, синдром Мириззи':
        await message.answer(message_texts.schema_3, reply_markup=ReplyKeyboardRemove(), parse_mode='Markdown')
    return None
