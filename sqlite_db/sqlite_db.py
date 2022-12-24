import sqlite3 as sq


def sql_start():
    global base, cur
    base = sq.connect('salon_koketka.db')
    cur = base.cursor()
    if base:
        print('Подключение к базе данных прошло успешно')
        base.execute('CREATE TABLE IF NOT EXISTS pricelist(img_id TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)')
        base.execute('CREATE TABLE IF NOT EXISTS admins_id(id TEXT)')
        base.commit()
    else:
        print('Произошла какая-то ошибка')


async def sql_add_command(data: dict):
    cur.execute('INSERT INTO pricelist VALUES(?, ?, ?, ?)', tuple(data.values()))
    base.commit()

async def sql_pricelist_command() -> list[tuple] | None:
    cur.execute('SELECT * FROM pricelist')
    return cur.fetchall()

async def sql_delete_command(name: str):
    cur.execute(f"DELETE FROM pricelist WHERE name = '{name}'")
    base.commit()

async def sql_change_command(name: str, item: str, new_value: str):
    cur.execute(f"UPDATE pricelist SET {item} = '{new_value}' where name = '{name}'")
    base.commit()

async def add_admin(id: str):
    cur.execute("INSERT INTO admins_id VALUES(?)", (id,))
    base.commit()

async def get_admins_id():
    cur.execute("SELECT id FROM admins_id")
    data = cur.fetchall()
    return data if data else [[]]