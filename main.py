import calc_before_operation
import calc_during_operation
import conversation
import asyncio

import create_patient, get_patients_
import faq
import holecystit
from states import UserInfo, HolecystitOperation, CreatePatient, ShowPatient, BeforeOperationFlow, DuringOperationFlow
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from buttons import FAQ_Callback

USER_TOKEN = '7174889644:AAE7uCtWLqle8mHgNfpHTotfj9GEwPw1jlQ'

async def start():
    bot = Bot(token=USER_TOKEN)
    await bot.delete_webhook(drop_pending_updates=True) # бот забывает все, что было до перезапуска

    dp = Dispatcher()

    dp.message.register(conversation.get_start, Command(commands='start'))

    # Главное меню
    dp.message.register(conversation.about_us, F.text == '⚕️ О нас')
    dp.message.register(conversation.get_faq, F.text == '❓FAQ')
    dp.message.register(holecystit.holecystit_start, F.text == '💊 Холецистит')
    dp.message.register(conversation.get_support, F.text == '🔨 Техническая поддержка')
    dp.message.register(create_patient.create_patient_start, F.text == '👨 Новый пациент')
    dp.message.register(get_patients_.get_patients, F.text == '👨‍👨‍👦 Все пациенты')
    dp.message.register(calc_before_operation.get_patients_bo, F.text == '⬆️ Предоперационный калькулятор')
    dp.message.register(calc_during_operation.get_patients_do, F.text == '⬇️ Интраоперационный калькулятор')


    # Создание пациента
    dp.message.register(create_patient.get_patient_name, CreatePatient.GET_NAME)
    dp.message.register(create_patient.get_patient_number, CreatePatient.GET_NUMBER)

    # Отображение информации по пациенту
    dp.message.register(get_patients_.show_patient_info, ShowPatient.SHOW_PATIENT)

    # Холецистит предоперационное флоу по пациенту
    dp.message.register(calc_before_operation.show_patient_info_bo, BeforeOperationFlow.SHOW_PATIENT)
    dp.message.register(calc_before_operation.holecystit_before_operation_1_bo, BeforeOperationFlow.STEP_1)
    dp.message.register(calc_before_operation.holecystit_before_operation_2_bo, BeforeOperationFlow.STEP_2)
    dp.message.register(calc_before_operation.holecystit_before_operation_3_bo, BeforeOperationFlow.STEP_3)
    dp.message.register(calc_before_operation.holecystit_before_operation_4_bo, BeforeOperationFlow.STEP_4)
    dp.message.register(calc_before_operation.holecystit_before_operation_5_bo, BeforeOperationFlow.STEP_5)
    dp.message.register(holecystit.show_schemas, BeforeOperationFlow.SCHEMAS)

    # Холецистит интраоперационнцый флоу по пациенту
    dp.message.register(calc_during_operation.show_patient_info_do, DuringOperationFlow.SHOW_PATIENT)
    dp.message.register(calc_during_operation.holecystit_during_operation_1_do, DuringOperationFlow.STEP_1)
    dp.message.register(calc_during_operation.holecystit_during_operation_2_do, DuringOperationFlow.STEP_2)
    dp.message.register(calc_during_operation.holecystit_during_operation_3_do, DuringOperationFlow.STEP_3)
    dp.message.register(calc_during_operation.holecystit_during_operation_4_do, DuringOperationFlow.STEP_4)
    dp.message.register(holecystit.show_schemas, DuringOperationFlow.SCHEMAS)

    # FAQ
    dp.callback_query.register(faq.what_bot_can, FAQ_Callback.filter(F.reply=='what_bot_can'))
    dp.callback_query.register(faq.how_reach_doс, FAQ_Callback.filter(F.reply=='how_reach_doc'))
    dp.callback_query.register(faq.back_to_faq, FAQ_Callback.filter(F.reply=='back_to_faq'))

    # Холецистит предоперационное флоу
    dp.message.register(holecystit.holecystit_before_operation_1, HolecystitOperation.STEP_1)
    dp.message.register(holecystit.holecystit_before_operation_2, HolecystitOperation.STEP_2)
    dp.message.register(holecystit.holecystit_before_operation_3, HolecystitOperation.STEP_3)
    dp.message.register(holecystit.holecystit_before_operation_4, HolecystitOperation.STEP_4)
    dp.message.register(holecystit.holecystit_before_operation_5, HolecystitOperation.STEP_5)

    # Холецистит интраоперационнцый флоу
    dp.message.register(holecystit.holecystit_during_operation_1, HolecystitOperation.STEP_6)
    dp.message.register(holecystit.holecystit_during_operation_2, HolecystitOperation.STEP_7)
    dp.message.register(holecystit.holecystit_during_operation_3, HolecystitOperation.STEP_8)
    dp.message.register(holecystit.holecystit_during_operation_4, HolecystitOperation.STEP_9)
    dp.message.register(holecystit.show_schemas, HolecystitOperation.STEP_10)


    # Регистрация врача
    dp.message.register(conversation.get_name, UserInfo.GET_NAME)
    dp.message.register(conversation.get_clinic, UserInfo.GET_CLINIC)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())