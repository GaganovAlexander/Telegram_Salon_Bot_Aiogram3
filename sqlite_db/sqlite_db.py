import sqlite3 as sq


def sql_start() -> None:
    """Creates/connect to sqlite database"""
    global base, cur
    base = sq.connect('salon.db')
    cur = base.cursor()
    if base:
        print('Подключение к базе данных прошло успешно')
        base.execute('CREATE TABLE IF NOT EXISTS pricelist(name TEXT PRIMARY KEY, description TEXT, price TEXT, num INTEGER)')
        base.commit()
    else:
        print('Произошла какая-то ошибка')


def sql_add_command(data: dict) -> None:
    """Adds row into pricelist table"""
    cur.execute('INSERT INTO pricelist(name, description, price, num) VALUES(?, ?, ?, 1)', tuple(data.values()))
    base.commit()

def sql_delete_command(name: str) -> None:
    """Deletes row and all of additional photos from db and photos dir"""
    cur.execute(f"DELETE FROM pricelist WHERE name = '{name}'")
    base.commit()

def sql_change_command(name: str, item: str, new_value: str) -> None:
    """Changes one item in choiced row"""
    cur.execute(f"UPDATE pricelist SET {item} = '{new_value}' WHERE name = '{name}'")
    base.commit()

def increase_num(name: str, num: int) -> None:
    """(De/In)crease num of photos in pricelist table"""
    if num < 0:
        cur.execute(f"UPDATE pricelist SET num = num - {-num} WHERE name = '{name}'")
    else:
        cur.execute(f"UPDATE pricelist SET num = num + {num} WHERE name = '{name}'")
    base.commit()
    
def get_num(name: str) -> list[tuple[int]]:
    """Returns num of all additional photos to choiced row"""
    cur.execute(f"SELECT num FROM pricelist WHERE name = '{name}'")
    data = cur.fetchall()
    return data if data else [()]

def get_all_names() -> list[tuple[str]]:
    cur.execute("SELECT name FROM pricelist")
    data = cur.fetchall()
    return data if data else [()]

def get_item(name: str) -> list[tuple[str]]:
    cur.execute(f"SELECT name, description, price FROM pricelist WHERE name = '{name}'")
    data = cur.fetchall()
    return data if data else [()]