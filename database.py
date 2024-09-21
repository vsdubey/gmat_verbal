import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_values
from config import DATABASE_URL
import logging
from embeddings import generate_question_embedding, generate_answer_embedding

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # Enable pgvector extension
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector")

        # Create questions table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id SERIAL PRIMARY KEY,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                source TEXT NOT NULL,
                difficulty TEXT NOT NULL
            )
        ''')

        # Create question_embeddings table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS question_embeddings (
                id SERIAL PRIMARY KEY,
                question_id INTEGER REFERENCES questions(id),
                question_embedding vector(1536),
                answer_embedding vector(1536)
            )
        ''')

        conn.commit()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
    finally:
        cur.close()
        conn.close()

def add_question(question, answer, source, difficulty):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            sql.SQL("INSERT INTO questions (question, answer, source, difficulty) VALUES (%s, %s, %s, %s) RETURNING id"),
            (question, answer, source, difficulty)
        )
        question_id = cur.fetchone()[0]
        
        question_embedding = generate_question_embedding({'question': question, 'answer': answer})
        answer_embedding = generate_answer_embedding({'question': question, 'answer': answer})
        
        if question_embedding and answer_embedding:
            cur.execute(
                sql.SQL("INSERT INTO question_embeddings (question_id, question_embedding, answer_embedding) VALUES (%s, %s, %s)"),
                (question_id, question_embedding, answer_embedding)
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

def get_similar_questions(query_embedding, limit=5):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('''
            SELECT q.id, q.question, q.answer, q.source, q.difficulty,
                   qe.question_embedding <-> %s AS distance
            FROM questions q
            JOIN question_embeddings qe ON q.id = qe.question_id
            ORDER BY distance
            LIMIT %s
        ''', (query_embedding, limit))
        similar_questions = cur.fetchall()
        return similar_questions
    except Exception as e:
        logger.error(f"Error getting similar questions: {str(e)}")
        return []
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
        
        question_embedding = generate_question_embedding({'question': question, 'answer': answer})
        answer_embedding = generate_answer_embedding({'question': question, 'answer': answer})
        
        if question_embedding and answer_embedding:
            cur.execute(
                sql.SQL("INSERT INTO question_embeddings (question_id, question_embedding, answer_embedding) VALUES (%s, %s, %s)"),
                (question_id, question_embedding, answer_embedding)
            )
        
        conn.commit()
        logger.info(f"Saved generated question: ID {question_id}")
        return question_id
    except Exception as e:
        logger.error(f"Error saving generated question: {str(e)}")
        return None
    finally:
        cur.close()
        conn.close()
