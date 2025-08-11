# Semantic Search with PostgreSQL & PGVector

This project is a complete end-to-end prototype of a semantic search engine. It uses a SentenceTransformer model to generate vector embeddings for text documents, stores them in a PostgreSQL database with the pgvector extension, and provides an interactive web interface built with Streamlit for searching.

## ✨ Live Demo

**[>> You can access the live application here <<](https://semantic-search-app-pgvector-dugevkoiipbuue7xcdfg4h.streamlit.app)**

## 🚀 Features

- **Scalable Data Ingestion:** Processes large text sources (CSV or folders of .txt files) in batches without high memory usage.
- **Vector Embeddings:** Uses the `all-MiniLM-L6-v2` model to create 384-dimensional embeddings.
- **Vector Database:** Leverages PostgreSQL and the `pgvector` extension with an HNSW index for high-performance similarity search.
- **Semantic Search:** Finds documents based on meaning, not just keywords.
- **Interactive UI:** A simple and user-friendly web interface built with Streamlit.
- **Command-Line Interface (CLI):** Includes a CLI for database setup, data ingestion, and searching.

## 🛠️ Technologies Used

- **Backend:** Python 3.13
- **Database:** PostgreSQL 16, pgvector
- **AI/ML:** Sentence-Transformers, PyTorch, Transformers
- **Web Framework:** Streamlit
- **Data Handling:** Pandas, NumPy
- **Database Driver:** psycopg2-binary
- **Deployment:** Neon (Database), Streamlit Community Cloud (Application)

## Local Setup and Usage

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/melihakdogan1/semantic-search-postgres-pgvector.git](https://github.com/melihakdogan1/semantic-search-postgres-pgvector.git)
    cd semantic-search-postgres-pgvector
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Set up your environment:**
    Create a `.env` file and fill it with your PostgreSQL database credentials.

4.  **Run the application:**
    - **Setup the database:**
      ```bash
      python main.py setup
      ```
    - **Ingest data:**
      ```bash
      python main.py ingest "path/to/your/data"
      ```
    - **Search via CLI:**
      ```bash
      python main.py search "your search query"
      ```
    - **Launch the web app:**
      ```bash
      streamlit run streamlit_app.py
      ```
