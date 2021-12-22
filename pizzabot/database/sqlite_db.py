import sqlite3 as sq


def sql_start():
    sql_file = './database/pizzabot.db'
    global base, cur
    base = sq.connect(sql_file)
    cur = base.cursor()
    if base:
        print('Database connected is OK!')
    base.executescript('''
        PRAGMA foreign_keys=on;
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            user_name TEXT NOT NULL,
            UNIQUE(user_id)
            );    
        CREATE TABLE IF NOT EXISTS users_orders(
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            product_type TEXT,
            size TEXT,
            pay TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id) 
            );
    ''')
    base.commit()


def add_user(id, name):
    sql_start()
    base.execute("INSERT OR IGNORE INTO users (user_id, user_name) values (?, ?)", (id, name))
    base.commit()

def add_order(usid, product, size, pay):
    sql_start()
    base.execute("INSERT INTO users_orders (user_id, product_type, size, pay) values (?, ?, ?, ?)", (usid, product, size, pay))
    base.commit()


async def show_order(message):
    for order in cur.execute(f'''SELECT id, product_type, size, pay FROM users_orders WHERE user_id={message.from_user.id}''').fetchall():
        await message.answer(f'Продукт: {order[1]}\nРазмер: {order[2]}\nОплата: {order[3]}')




if __name__ == '__main__':
    sql_start()









