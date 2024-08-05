from aiogram.fsm.state import StatesGroup, State

class UserInfo(StatesGroup):
    GET_NAME=State()
    GET_CLINIC=State()

class HolecystitOperation(StatesGroup):
    STEP_1 = State()
    STEP_2 = State()
    STEP_3 = State()
    STEP_4 = State()
    STEP_5 = State()
    STEP_6 = State()
    STEP_7 = State()
    STEP_8 = State()
    STEP_9 = State()
    STEP_10 = State()

class CreatePatient(StatesGroup):
    GET_NAME = State()
    GET_NUMBER = State()

class ShowPatient(StatesGroup):
    SHOW_PATIENT = State()

class BeforeOperationFlow(StatesGroup):
    SHOW_PATIENT = State()
    STEP_1 = State()
    STEP_2 = State()
    STEP_3 = State()
    STEP_4 = State()
    STEP_5 = State()
    SCHEMAS = State()
class DuringOperationFlow(StatesGroup):
    SHOW_PATIENT = State()
    STEP_1 = State()
    STEP_2 = State()
    STEP_3 = State()
    STEP_4 = State()
    SCHEMAS = State()
