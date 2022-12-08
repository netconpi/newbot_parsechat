import sqlite3


def connect():
    try:
        connection = sqlite3.connect('data.db')
        return connection
    except:
        return 0


def add_offer(name, tg_id, text, source):
    con = connect()
    cur = con.cursor()

    cur.execute(
        f"INSERT INTO messages (text, tg_id, namee) VALUES ('{text}', {tg_id}, '{name}')"
    )

    con.commit()


def add_me(tg_id):
    con = connect()
    cur = con.cursor()

    cur.execute(
        f"INSERT INTO verify (tg_id) VALUES ({tg_id})"
    )

    con.commit()


def get_all_users():
    con = connect()
    cur = con.cursor()

    # Tabels 
    # acc_garanted
    # verify

    cur.execute("SELECT tg_id FROM acc_garanted")
    garanted_list = cur.fetchall()

    cur.execute("SELECT tg_id FROM verify")
    verify_list = cur.fetchall()

    return garanted_list, verify_list


def checkuser_status(tg_id):
    con = connect()
    cur = con.cursor()

    # Tabels 
    # acc_garanted
    # verify

    cur.execute(f"SELECT tg_id FROM acc_garanted WHERE tg_id={tg_id}")
    garanted_list = cur.fetchall()

    cur.execute(f"SELECT tg_id FROM verify WHERE tg_id={tg_id}")
    verify_list = cur.fetchall()

    if garanted_list:
        return 1
    if verify_list:
        return 0


def remove_from_list(tg_id):
    con = connect()
    cur = con.cursor()
    if checkuser_status(tg_id):
        cur.execute(f"DELETE FROM acc_garanted WHERE tg_id={tg_id}")
    else: 
        cur.execute(f"DELETE FROM verify WHERE tg_id={tg_id}")

    con.commit()


def add_accs(tg_id):
    con = connect()
    cur = con.cursor()
    
    cur.execute(f"DELETE FROM verify WHERE tg_id={tg_id}")
    con.commit()

    cur.execute(f"INSERT INTO acc_garanted (tg_id) VALUES ({tg_id})")
    con.commit()


def add_kw(word):
    con = connect()
    cur = con.cursor()
    
    cur.execute(f"INSERT INTO keywords (word) VALUES ('{word}')")
    con.commit()


def remove_kw(word):
    con = connect()
    cur = con.cursor()
    
    cur.execute(f"DELETE FROM keywords WHERE word='{word}'")
    con.commit()


def get_kw():
    con = connect()
    cur = con.cursor()

    cur.execute('SELECT * FROM keywords')
    txt_out = "Список ключевых слов. \nID - Ключевое слово\n"
    res = cur.fetchall()

    for i in res:
        txt_out += f"{i[0]} - {i[1]}\n"

    return txt_out

def get_word(idd):
    con = connect()
    cur = con.cursor()

    cur.execute(f'SELECT word FROM keywords WHERE id={idd}')
    res = cur.fetchall()

    if res:
        return res[0][0]
    else:
        return 0


def get_kw_list():
    con = connect()
    cur = con.cursor()

    cur.execute(f'SELECT word FROM keywords')
    res = cur.fetchall()
    kw_list = []

    for i in res:
        kw_list.append(i[0])

    return kw_list