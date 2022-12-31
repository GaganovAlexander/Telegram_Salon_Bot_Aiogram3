from aiogram.utils.keyboard import InlineKeyboardBuilder


def admin_items_inlines(name: str):
    """Returns inline keyboard for admin's /check_pricelist command"""
    kb = InlineKeyboardBuilder()

    kb.button(text='Добавить больше фотографий', callback_data=f'add_{name}')
    
    kb.button(text='Изменить фото', callback_data=f'change_photo_{name}')
    kb.button(text='Изменить имя', callback_data=f'change_name_{name}')
    kb.button(text='Изменить описание', callback_data=f'change_description_{name}')
    kb.button(text='Изменить цену', callback_data=f'change_price_{name}')
    kb.button(text='Удалить фото из списка дополнительных', callback_data=f"deletephoto_{name}")

    kb.button(text='Удалить пункт', callback_data=f'delete_{name}')

    kb.adjust(1, 2, 2, 1, 1)
    return kb.as_markup()

def admin_photo_inlines(num: int, name: str, mode: str = 'mainphoto'):
    """Returns inline keyboard for admin to change main photo/delete additional photos"""
    if not num:
        return
    if mode == 'choice':
        add = 1
    else:
        add = 0
    kb = InlineKeyboardBuilder()
    index = 0
    adjust = []
    for i in range(num):
        if i and not i % 4:
            adjust.append(4)
        kb.button(text=f"{i+1}", callback_data=f"{mode}_{i+add}_{name}")
        index += 1

    if num % 4:
        adjust.append(num % 4)
    
    if mode == 'mainphoto':
        kb.button(text="Загрузить новое главное фото", callback_data=f'new_{name}')
        adjust.append(1)
    kb.adjust(*adjust)
    return kb.as_markup()

def client_items_inlines(name: str):
    """Returns inline keyboard for client's /pricelist command"""
    kb = InlineKeyboardBuilder()

    kb.button(text='Больше фото', callback_data=f'photos_{name}')
    kb.button(text='Записаться', callback_data=f'book_{name}')

    kb.adjust(1, 1)
    return kb.as_markup()