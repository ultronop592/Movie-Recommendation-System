import pandas as pd
import numpy as np
import logging
from scipy.sparse import load_npz
from pathlib import Path

# Get the directory where this script is located
script_dir = Path(__file__).parent

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(script_dir / "recommend.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logging.info("🔁 Loading data...")
try:
    # Load the processed movie data
    movie = pd.read_parquet(script_dir / 'cleaned.parquet')
    
    # Load the cosine similarity matrix (sparse format)
    cosine_sim_sparse = load_npz(script_dir / 'cosine_sim.npz')
    # Convert to dense for easier indexing
    cosine_sim = cosine_sim_sparse.toarray()
    
    logging.info("✅ Data loaded successfully.")
except Exception as e:
    logging.error("❌ Failed to load required files: %s", str(e))
    raise e


def recommend_movies(movie_name, top_n=7):
    logging.info("🎬 Recommending movies for: '%s'", movie_name)
    idx = movie[movie['title'] == movie_name].index.tolist()
    if len(idx) == 0:
        logging.warning("⚠️ Movie not found in dataset.")
        return None
    idx = idx[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n + 1]
    movie_indices = [i[0] for i in sim_scores]
    logging.info("✅ Top %d recommendations ready.", top_n)
    
    
    
    
    # Create DataFrame with clean serial numbers starting from 1
    result_df = movie[['title']].iloc[movie_indices].reset_index(drop=True)
    result_df.index = result_df.index + 1  # Start from 1 instead of 0
    result_df.index.name = "S.No."

    return result_df