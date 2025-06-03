import sqlite3

with sqlite3.connect("database.db") as conn:
    cur = conn.cursor()

    cur.execute("""
    DROP TABLE singleagents;
    """)
    conn.commit()