# preprocess.py
import pandas as pd
import numpy as np
import re
import nltk
import logging
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import save_npz


# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("preprocess.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logging.info("🚀 Starting preprocessing...")

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

# Text cleaning
stop_words = set(stopwords.words('english'))

# Load and sample dataset
try:
    movie = pd.read_csv('movies.csv')
    logging.info("✅ Dataset loaded successfully. Total rows: %d", len(movie))
except Exception as e:
    logging.error("❌ Failed to load dataset: %s", str(e))
    raise e

def preprocess_text(text):
    text = re.sub(r"[^a-zA-Z\s]", "", str(text))
    text = text.lower()
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stop_words]
    return " ".join(tokens)


# filter the required columns for recommendation
new_columns =["genres","keywords","overview", "title"]

movie = movie[new_columns]

movie = movie.dropna().reset_index(drop=True)

movie["combined"] = movie["genres"] + " " + movie["keywords"] + " " + movie["overview"]

logging.info("🧹 Cleaning text...")
movie['cleaned_text'] = movie['combined'].apply(preprocess_text)
logging.info("✅ Text cleaned.")


# Vectorization
logging.info("🔠 Vectorizing using TF-IDF...")
tfidf = TfidfVectorizer(max_features=5000)
tfidf_matrix = tfidf.fit_transform(movie['cleaned_text'])
logging.info("✅ TF-IDF matrix shape: %s", tfidf_matrix.shape)

# Cosine similarity
logging.info("📐 Calculating cosine similarity...")
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
logging.info("✅ Cosine similarity matrix generated.")

# Save in more compatible formats
logging.info("💾 Saving files in compatible formats...")

# Save movie dataset as parquet
movie.to_parquet('cleaned.parquet', compression='gzip')

# Convert dense similarity matrix to sparse (only keep significant similarities)
threshold = 0.5  # Only keep strong similarities above this threshold
sparse_sim = cosine_sim.copy()
sparse_sim[sparse_sim < threshold] = 0
from scipy.sparse import csr_matrix
sparse_sim = csr_matrix(sparse_sim)
save_npz('cosine_sim.npz', sparse_sim)

# Save TF-IDF matrix as sparse matrix
save_npz('tfidf_matrix.npz', tfidf_matrix)

logging.info("💾 Data saved to disk.")
logging.info("✅ Preprocessing complete.")