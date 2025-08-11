import os
import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import execute_values

# PostgreSQL Connection
def get_db_connection():
    load_dotenv()
    conn = psycopg2.connect(
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    return conn

# Prepare the table
def setup_database():
    conn = get_db_connection()
    cur = conn.cursor()

    print("Doing the database setup...")

    cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    print("-> vector plugin active")

    # Create documents_embedding table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS documents_embedding
        (
            id serial PRIMARY KEY,
            document_text TEXT,
            embedding vector(384),
            hash character varying(64) UNIQUE
        );
    """)
    print("-> documents_embedding table ready")

    conn.commit()
    cur.close()
    conn.close()
    print("Setup completed")

# Adds a single document to the database
def insert_document(cursor, doc_text, doc_embedding, doc_hash):
    cursor.execute("""
        INSERT INTO documents_embedding (document_text, embedding, hash)
        VALUES (%s, %s, %s)
        ON CONFLICT (hash) DO NOTHING
    """, (doc_text, doc_embedding, doc_hash))

# Find the most similar documents in the query vector
def search_similar_documents(query_embedding, top_n=5):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            document_text,
            1 - (embedding <=> %s) AS similarity
        FROM
            documents_embedding
        ORDER BY
            similarity DESC
        LIMIT %s;
    """, (str(query_embedding), top_n))

    results = cur.fetchall()
    cur.close()
    conn.close()
    return results

# Adds the document list to the database in bulk
def insert_documents_batch(documents):
    conn = get_db_connection()
    cur = conn.cursor()

    execute_values(
        cur,
        """
        INSERT INTO documents_embedding(document_text, embedding, hash)
        VALUES %s
        ON CONFLICT (hash) DO NOTHING;
        """,
        documents
    )
    conn.commit()
    cur.close()
    conn.close()
    print(f"Successfully inserted a batch of {len(documents)} documents")
