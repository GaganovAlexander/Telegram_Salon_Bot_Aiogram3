import sqlite3 as sq
from shutil import rmtree

async def sql_start() -> None:
    """Creates/connect to sqlite database"""
    global base, cur
    base = sq.connect('salon_koketka.db')
    cur = base.cursor()
    if base:
        print('Подключение к базе данных прошло успешно')
        base.execute('CREATE TABLE IF NOT EXISTS pricelist(name TEXT PRIMARY KEY, description TEXT, price TEXT, num INTEGER)')
        base.execute('CREATE TABLE IF NOT EXISTS admins_id(id TEXT)')
        base.commit()
    else:
        print('Произошла какая-то ошибка')


async def sql_add_command(data: dict) -> None:
    """Adds row into pricelist table"""
    cur.execute('INSERT INTO pricelist VALUES(?, ?, ?, 1)', tuple(data.values()))
    base.commit()

async def sql_pricelist_command() -> list[tuple[str]]:
    """Returns list of tuples(rows) in table pricelist: name, description, price"""
    cur.execute('SELECT name, description, price FROM pricelist')
    return cur.fetchall()

async def sql_delete_command(name: str) -> None:
    """Deletes row and all of additional photos from db and photos dir"""
    cur.execute(f"DELETE FROM pricelist WHERE name = '{name}'")
    base.commit()
    rmtree(f"photos/{name}")

async def sql_change_command(name: str, item: str, new_value: str) -> None:
    """Changes one item in choiced row"""
    cur.execute(f"UPDATE pricelist SET {item} = '{new_value}' WHERE name = '{name}'")
    base.commit()

async def add_admin(id: str) -> None:
    """Adds an user id to the admins ids"""
    cur.execute("INSERT INTO admins_id VALUES(?)", (id,))
    base.commit()

async def increase_num(name: str, num: int) -> None:
    """(De/In)crease num of photos in pricelist table"""
    if num < 0:
        cur.execute(f"UPDATE pricelist SET num = num - {-num} WHERE name = '{name}'")
    else:
        cur.execute(f"UPDATE pricelist SET num = num + {num} WHERE name = '{name}'")
    base.commit()
    
async def get_num(name: str) -> list[tuple[int]]:
    """Returns num of all additional photos to choiced row"""
    cur.execute(f"SELECT num FROM pricelist WHERE name = '{name}'")
    return cur.fetchall()

async def get_admins_id() -> list[tuple[str]]:
    """Returns list of all admins ids(they are the single item in the tuples)"""
    cur.execute("SELECT id FROM admins_id")
    data = cur.fetchall()
    return data if data else [()]