import psycopg2
from psycopg2 import sql

# Database connection parameters
db_params = {
    "host": "localhost",
    "port": 5432,  
    "database": "llm_guardrail",
    "user": "postgres",
    "password": "Ryanrj@37"
}

from psycopg2 import pool

connection_pool = psycopg2.pool.SimpleConnectionPool(1, 10, **db_params)

def logging(promptid, prompt, jailbreak, flag,session_id):
    #print("Logging to DB:", userid, prompt, jailbreak, flag, session_id)
    conn = None
    try:
        conn = connection_pool.getconn()
        cur = conn.cursor()
        print("Database connection established.")

        insert_query = """
        INSERT INTO Logs (prompt_id, prompt, jailbreak, word_flagged,session_id)
        VALUES (%s, %s, %s, %s,%s)
        """
        flags = [flag]

        cur.execute(insert_query, (promptid, prompt, jailbreak, flags,session_id))
        conn.commit()

        cur.close()
    except Exception as e:
        print("Error inserting data:", e)
        if conn:
            conn.rollback()
    finally:
        if conn:
            connection_pool.putconn(conn)
