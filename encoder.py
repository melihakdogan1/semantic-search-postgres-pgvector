from sentence_transformers import SentenceTransformer
import hashlib

MODEL = None

# Loads the SentenceTransformer model or returns it if it exists in memory
def get_model():
    global MODEL
    if MODEL is None:
        print("Loading the embedding model... (This process may take a while the first time.)")
        MODEL = SentenceTransformer('all-MiniLM-L6-v2')
        print("Model loaded")
    return MODEL

# Converts a given text to embedding
def encode_texts(texts):
    model = get_model()
    return model.encode(texts).tolist()

# Creates a hash of a single given text
def encode_text_hash(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()





