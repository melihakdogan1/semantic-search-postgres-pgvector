import pandas as pd
import database as db
import encoder as enc
import argparse
from pathlib import Path
from itertools import islice

# Reads the sources on the given path one by one using 'yield'
def read_data_source(path: Path):
    if path.is_dir():
        print(f"Reading .txt files from folder '{path}'...")
        for file_path in path.glob("*.txt"):
            with open(file_path, 'r', encoding='utf-8') as f:
                yield f.read()
    elif path.is_file() and path.suffix == '.csv':
        print(f"Reading data from CSV file '{path}'...")
        df = pd.read_csv(path)
        for text in df['document_text']:
            yield text

# Takes an iterator and splits it into baches of the specified size
def batch_generator(iterator, batch_size):
    while True:
        batch = list(islice(iterator, batch_size))
        if not batch:
            break
        yield batch

# Runs the data pipeline: reads data, groups it, processes it and inserts it into the database
def ingest_data(data_path: str, batch_size: int = 128):
    path = Path(data_path)
    if not path.exists():
        print(f"Error: The specified path was not found: {data_path}")
        return

    data_iterator = read_data_source(path)

    total_processed = 0
    for text_batch in batch_generator(data_iterator, batch_size):
        # 1. Process text group
        embeddings = enc.encode_texts(text_batch)

        # 2. Prepare the format to be added to the database
        documents_to_insert = []
        for i, text in enumerate(text_batch):
            doc_hash = enc.encode_text_hash(text)
            documents_to_insert.append((text, embeddings[i], doc_hash))
        
        # 3. Add the group to the database in bulk
        db.insert_documents_batch(documents_to_insert)
        total_processed += len(text_batch)
        print(f"{total_processed} documents processed and added to the database...")
    
    print("All data loading operations are completed")

# Performs semantic search for a given query and prints the results
def search_data(query: str, top_n: int = 3):
    print(f"\nQuery: '{query}'")
    print("Searching similar results...")
    print("-"*20)

    query_embedding = enc.encode_texts([query])[0]
    results = db.search_similar_documents(query_embedding, top_n=top_n)

    if not results:
        print("No results found")
        return

    for doc in results:
        doc_id, doc_text, doc_similarity = doc
        print(f"ID: {doc_id} | Similarity Score: {float(doc_similarity):.4f}")
        print(f"Text: {doc_text}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Semantic Search Project with PostgreSQL and Vector Embeddings")

    # setup, ingest, search
    subparsers = parser.add_subparsers(dest='command', required=True, help='Command to execute')

    # setup command
    parser_setup = subparsers.add_parser('setup', help='Prepares the database and table for initial setup')

    # ingest command
    parser_ingest = subparsers.add_parser('ingest', help='Processes the data in the specified path (.csv or folder) and adds it to the database')
    parser_ingest.add_argument('path', type=str, help='Path to the data source (folder containing csv files or .txt files)')
    parser_ingest.add_argument('--batch_size', type=int, default=128, help='Number of documents to be processed at one time')

    # search command
    parser_search = subparsers.add_parser('search', help='Performs semantic search in the database')
    parser_search.add_argument('query', type=str, help='Text or question to search')
    parser_search.add_argument('--top_n', type=int, default=3, help='Number of most similar results to be returned')

    args = parser.parse_args()

    if args.command == 'setup':
        db.setup_database()
    elif args.command == 'ingest':
        ingest_data(args.path, args.batch_size)
    elif args.command == 'search':
        search_data(args.query, args.top_n)

