from aiogram.types import CallbackQuery
import message_texts
from buttons import back_to_faq_button, faq_buttons

async def what_bot_can(call: CallbackQuery):
    await call.message.edit_text(message_texts.what_bot_can_text, reply_markup=back_to_faq_button, parse_mode='Markdown')
    return None
async def how_reach_doс(call: CallbackQuery):
    await call.message.edit_text(message_texts.how_reach_doс_text, reply_markup=back_to_faq_button, parse_mode='Markdown')
    return None
async def back_to_faq(call: CallbackQuery):
    await call.message.edit_text(message_texts.faq_text, reply_markup=faq_buttons)
    return None
