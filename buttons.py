from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData

class FAQ_Callback(CallbackData, prefix="faq"):
    reply: str

initial_keyboard = [
    [
        KeyboardButton(text='💊 Холецистит')
        , KeyboardButton(text='⚕️ О нас')
        ],
    [
        KeyboardButton(text='👨 Новый пациент')
        , KeyboardButton(text='👨‍👨‍👦 Все пациенты')
    ],
    [
        KeyboardButton(text='⬆️ Предоперационный калькулятор')
        , KeyboardButton(text='⬇️ Интраоперационный калькулятор')
    ],
    [
        KeyboardButton(text='🔨 Техническая поддержка', url='t.me/mgadziev')
        , KeyboardButton(text='❓FAQ')
    ],
    [
        KeyboardButton(text='Оставить комментарий по пациенту')
    ]
]
initial_keyboard_markup = ReplyKeyboardMarkup(keyboard=initial_keyboard, resize_keyboard=True)

# FAQ
faq_buttons = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Что умеет бот?', callback_data=FAQ_Callback(reply='what_bot_can').pack())],
    [InlineKeyboardButton(text="Как мне связаться с врачами?", callback_data=FAQ_Callback(reply='how_reach_doc').pack())]
]
)

back_to_faq_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Вернуться', callback_data=FAQ_Callback(reply='back_to_faq').pack())],
]
)

# Техническая поддержка

tech_support_buttons = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📝 Написать модератору", url='t.me/mgadziev')]])

# Опросник
yes_no = [
    [
        KeyboardButton(text='Да')
        , KeyboardButton(text='Нет')
        ],
    [
        KeyboardButton(text='Главное меню')
    ]
]
yes_no_markup = ReplyKeyboardMarkup(keyboard=yes_no, resize_keyboard=True)

menu = [
    [
        KeyboardButton(text='Главное меню')
    ]
]
menu_markup = ReplyKeyboardMarkup(keyboard=yes_no, resize_keyboard=True)



holicestit_organization_level_keyboard = [
    [
        KeyboardButton(text='Поликлинический уровень')
        , KeyboardButton(text='Медицинская организация II уровня')
        ],
    [
        KeyboardButton(text='Окружной стационар II уровня')
        , KeyboardButton(text='Медицинская организация III уровня')
    ]
]
holicestit_organization_level_markup = ReplyKeyboardMarkup(keyboard=holicestit_organization_level_keyboard, resize_keyboard=True)

schema_keyboard = [
    [
        KeyboardButton(text='ЖКБ, осложненная холедохолитиазом')
        , KeyboardButton(text='Трудная анатомия')
        , KeyboardButton(text='Сморщенный пузырь, синдром Мириззи')
    ]
]
schema_keyboard_markup = ReplyKeyboardMarkup(keyboard=schema_keyboard, resize_keyboard=True)
