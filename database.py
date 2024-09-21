import psycopg2
from psycopg2 import sql
from config import DATABASE_URL
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    logger.info("Database initialized successfully")

def add_question(question, answer, source, difficulty):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            sql.SQL("INSERT INTO questions (question, answer, source, difficulty) VALUES (%s, %s, %s, %s)"),
            (question, answer, source, difficulty)
        )
        conn.commit()
        logger.info(f"Added question: {question[:100]}...")
        logger.info(f"Answer: {answer[:100]}...")
        logger.info(f"Source: {source}, Difficulty: {difficulty}")
    except Exception as e:
        logger.error(f"Error adding question: {str(e)}")
    finally:
        cur.close()
        conn.close()

def get_random_question():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM questions")
        total_questions = cur.fetchone()[0]
        logger.info(f"Total number of questions in the database: {total_questions}")

        cur.execute("SELECT * FROM questions ORDER BY RANDOM() LIMIT 1")
        question = cur.fetchone()
        if question:
            logger.info(f"Retrieved random question: ID {question[0]}")
        else:
            logger.warning("No questions available in the database")
        return question
    except Exception as e:
        logger.error(f"Error getting random question: {str(e)}")
        return None
    finally:
        cur.close()
        conn.close()

def save_generated_question(question, answer, difficulty):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            sql.SQL("INSERT INTO questions (question, answer, source, difficulty) VALUES (%s, %s, %s, %s) RETURNING id"),
            (question, answer, 'AI', difficulty)
        )
        question_id = cur.fetchone()[0]
        conn.commit()
        logger.info(f"Saved generated question: ID {question_id}")
        return question_id
    except Exception as e:
        logger.error(f"Error saving generated question: {str(e)}")
        return None
    finally:
        cur.close()
        conn.close()
