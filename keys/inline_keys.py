from aiogram.utils.keyboard import InlineKeyboardBuilder


def items_inlines(name: str):
    kb = InlineKeyboardBuilder()

    kb.button(text='Изменить фото', callback_data=f'cnahge_photo_{name}')
    kb.button(text='Изменить имя', callback_data=f'cnahge_name_{name}')
    kb.button(text='Изменить описание', callback_data=f'cnahge_description_{name}')
    kb.button(text='Изменить цену', callback_data=f'cnahge_price_{name}')

    kb.button(text='Удалить', callback_data=f'delete_{name}')

    kb.adjust(2, 2, 1)
    return kb.as_markup()