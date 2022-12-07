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
