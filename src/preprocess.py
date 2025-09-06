# preprocess.py
import pandas as pd
import re
import nltk
import joblib
import logging
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


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

# Save with maximum compression
logging.info("💾 Saving files with maximum compression...")
joblib.dump(movie, 'cleaned.pkl', compress=('gzip', 9))  # Maximum compression
joblib.dump(tfidf_matrix, 'tfidf_matrix.pkl', compress=('gzip', 9))
joblib.dump(cosine_sim, 'cosine_sim.pkl', compress=('gzip', 9))
logging.info("💾 Data saved to disk.")
logging.info("✅ Preprocessing complete.")