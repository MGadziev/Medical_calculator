import datetime, os

from sqlalchemy import create_engine, Column, String, DateTime, Boolean, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(String, primary_key=True)
    tg_name = Column(String)
    created_at = Column(DateTime)
    name = Column(String)
    clinic = Column(String)

async def create_user(user_id, tg_name, name, clinic):
    try:
        user = session.query(User).filter_by(user_id=str(user_id)).first()
        if user:
            return 1
        else:
            created_at = datetime.datetime.now()
            new_client = User(user_id=str(user_id), tg_name=tg_name, created_at=created_at, name=name, clinic=clinic)
            session.add(new_client)
            session.commit()
            return 0
    except Exception as e:
        print(f"Ошибка при создании нового пользователя: {e}")

async def check_user(user_id):
    try:
        user = session.query(User).filter_by(user_id=str(user_id)).first()
        if user:
            return 1
        else:
            return 0
    except Exception as e:
        print(f"Ошибка при создании нового пользователя: {e}")

class Patient(Base):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    card_number = Column(String)
    status = Column(String, default='new')
    created_at = Column(DateTime)
    holicestit_organization_level = Column(String)
    age_more_than_55 = Column(Boolean, default=False)
    imt_more_than_30 = Column(Boolean,  default=False)
    stoma_operations = Column(Boolean, default=False)
    jaundice = Column(Boolean, default=False)
    adhesion = Column(Boolean, default=False)
    omentum = Column(Boolean, default=False)
    fibrose_changes = Column(Boolean, default=False)
    infiltrat = Column(Boolean, default=False)
    doctor_id = Column(String)
    total_score = Column(Integer, default=0)

async def create_patient(name, card_number, doctor_id):
    try:
        created_at = datetime.datetime.now()
        new_patient = Patient(name=name, card_number=card_number, created_at=created_at, doctor_id = doctor_id)
        session.add(new_patient)
        session.commit()
        return 1
    except Exception as e:
        print(f"Ошибка при создании нового пациента: {e}")
        return None

async def get_patients_info(doctor_id, status=None):
    try:
        if status:
            patients = session.query(Patient).filter_by(status=status, doctor_id=doctor_id).all()
        else:
            patients = session.query(Patient).filter_by(doctor_id=doctor_id).all()
        if patients:
            return patients
        else:
            return None
    except Exception as e:
        print(f"Ошибка при создании получении информации по пациентам: {e}")

async def get_patients_info_by_id(id):
    try:
        patient = session.query(Patient).filter_by(id=id).first()
        if patient:
            return patient
        else:
            return None
    except Exception as e:
        print(f"Ошибка при создании получении информации по пациенту: {e}")



async def update_patient_by_id(patient_id, new_status=None, holicestit_organization_level=None, age_more_than_55=None
                               , imt_more_than_30=None, stoma_operations=None, jaundice=None, adhesion=None,
                               omentum=None, fibrose_changes=None, infiltrat=None, total_score=None):
    try:
        patient = session.query(Patient).filter_by(id=patient_id).first()
        if patient:
            if new_status:
                patient.status = new_status
            if holicestit_organization_level:
                patient.holicestit_organization_level = holicestit_organization_level
            if age_more_than_55:
                patient.age_more_than_55 = age_more_than_55
            if imt_more_than_30:
                patient.imt_more_than_30 = imt_more_than_30
            if stoma_operations:
                patient.stoma_operations = stoma_operations
            if jaundice:
                patient.jaundice = jaundice
            if adhesion:
                patient.adhesion = adhesion
            if omentum:
                patient.omentum = omentum
            if fibrose_changes:
                patient.fibrose_changes = fibrose_changes
            if infiltrat:
                patient.infiltrat = infiltrat
            if total_score:
                patient.total_score = total_score
            session.commit()
        return None
    except Exception as e:
        error_message = f"⚠️Ошибка при изменении заявки [sell_usdt]: {str(e)}"
        print(error_message)
        session.rollback()
        return None

# Создаем соединение с базой данных
engine = create_engine(f"{os.environ.get('DB_SERVER')}")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
