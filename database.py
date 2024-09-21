import psycopg2
from psycopg2 import sql
from config import DATABASE_URL

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id SERIAL PRIMARY KEY,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            source TEXT NOT NULL,
            difficulty TEXT NOT NULL
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

def add_question(question, answer, source, difficulty):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        sql.SQL("INSERT INTO questions (question, answer, source, difficulty) VALUES (%s, %s, %s, %s)"),
        (question, answer, source, difficulty)
    )
    conn.commit()
    cur.close()
    conn.close()

def get_random_question():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM questions ORDER BY RANDOM() LIMIT 1")
    question = cur.fetchone()
    cur.close()
    conn.close()
    return question

def save_generated_question(question, answer, difficulty):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        sql.SQL("INSERT INTO questions (question, answer, source, difficulty) VALUES (%s, %s, %s, %s) RETURNING id"),
        (question, answer, 'AI', difficulty)
    )
    question_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return question_id
