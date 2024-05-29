# db.database.py
from contextlib import contextmanager
import psycopg2
from psycopg2.extras import DictCursor
# Database connection parameters
DATABASE_NAME = "question_answers"
DATABASE_USER = "codewithme"
DATABASE_PASSWORD = "lotfy01@"
DATABASE_HOST = "localhost"
DATABASE_PORT = "5432"

# Establish a connection to the database
def get_db_connection():
    conn = psycopg2.connect(
        dbname=DATABASE_NAME,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        port=DATABASE_PORT
    )
    return conn

# Context manager to manage database cursor
@contextmanager
def get_db_cursor():
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            yield cursor
    finally:
        conn.close()

# Function to create the question_answers table if it doesn't exist
def create_table():
    query = """
    CREATE TABLE IF NOT EXISTS question_answers (
        id SERIAL PRIMARY KEY,
        question TEXT NOT NULL,
        user_answer TEXT NOT NULL,
        score FLOAT NOT NULL
    );
    """
    with get_db_cursor() as cursor:
        cursor.execute(query)
        cursor.connection.commit()

# Ensure the table is created when the module is imported
create_table()

# Define database operations
def save_question_answer(question, user_answer, score):
    query = """
    INSERT INTO question_answers (question, user_answer, score)
    VALUES (%s, %s, %s)
    """
    with get_db_cursor() as cursor:
        cursor.execute(query, (question, user_answer, score))
        cursor.connection.commit()


def save_questions_and_answers_and_scores(questions, answers, scores):
    query = """
    INSERT INTO question_answers (question, user_answer, score)
    VALUES (%s, %s, %s)
    """
    with get_db_cursor() as cursor:
        for question, answer, score in zip(questions, answers, scores):
            cursor.execute(query, (question, answer, score))
        cursor.connection.commit()



def get_question_answers():
    query = "SELECT * FROM question_answers"
    with get_db_cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()

def get_question_answer(question_id):
    query = "SELECT * FROM question_answers WHERE id = %s"
    with get_db_cursor() as cursor:
        cursor.execute(query, (question_id,))
        return cursor.fetchone()

def delete_question_answer(question_id):
    query = "DELETE FROM question_answers WHERE id = %s"
    with get_db_cursor() as cursor:
        cursor.execute(query, (question_id,))
        cursor.connection.commit()

def delete_question_answers():
    query = "DELETE FROM question_answers"
    with get_db_cursor() as cursor:
        cursor.execute(query)
        cursor.connection.commit()


# Existing code remains unchanged...

def get_question(question_id):
    query = "SELECT question FROM question_answers WHERE id = %s"
    with get_db_cursor() as cursor:
        cursor.execute(query, (question_id,))
        return cursor.fetchone()