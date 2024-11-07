import aiosqlite


async def add_user(user_id):
    connect = await aiosqlite.connect('escadrobot.db')
    cursor = await connect.cursor()
    check_user = await cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id))
    check_user = await check_user.fetchone()
    if check_user is None:
        await cursor.execute('INSERT INTO users (user_id) VALUES (?)', (user_id))
        print(f'''Пользователь c id {user_id}
              добавлен в базу данных (таблица users).''')
        await connect.commit()
    await cursor.close()
    await connect.close()


async def add_ticket(id, theme, status, auhtor, anydesk_id):
    connect = await aiosqlite.connect('escadrobot.db')
    cursor = await connect.cursor()
    await cursor.execute('INSERT INTO tickets (id, theme, status, auhtor, anydesk_id) VALUES (?, ?, ?, ?, ?)', (id, theme, status, auhtor, anydesk_id))
    print(f'''Тикет "{theme}" c id {
          id} добавлен в базу данных (таблица tickets).''')
    await connect.commit()
    await cursor.close()
    await connect.close()


async def get_user_ids():
    connect = await aiosqlite.connect('escadrobot.db')
    cursor = await connect.cursor()
    active_ids = await cursor.execute('SELECT user_id FROM users')
    await cursor.close()
    await connect.close()
    return active_ids
