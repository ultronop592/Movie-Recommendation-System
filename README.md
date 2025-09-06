# Movie Recommendation System

A movie recommendation system built with Python, Streamlit, and OMDB API integration.

## Pre-trained Model Files
Some model files are required for the system to work:

Already included in the repository:
- `src/cleaned.pkl`: Processed movie dataset (included)

Not included due to size limitations:
- `src/cosine_sim.pkl`: Pre-computed similarity matrix (needs to be generated)
- `src/tfidf_matrix.pkl`: TF-IDF vectors for movies (needs to be generated)

You can either:
1. Download the pre-trained files from [Release Assets](https://github.com/ultronop592/Movie-Recommendation-System/releases)
   - Download the files from the latest release
   - Place them in the `src` directory
   OR
2. Generate them yourself using the preprocessing script (see Setup Instructions below)

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/ultronop592/Movie-Recommendation-System.git
cd Movie-Recommendation-System
```

2. Create a virtual environment and activate it:
```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up the model files:
   - Option 1: Download pre-trained files from [Releases](https://github.com/ultronop592/Movie-Recommendation-System/releases)
   - Option 2: Generate them yourself:
     1. Place your movies dataset (CSV file) in the `src` directory as `movies.csv`
     2. Run the preprocessing script:
     ```bash
     cd src
     python preprocess.py
     ```

5. Get your OMDB API key from [omdbapi.com](http://www.omdbapi.com/) and add it to `src/config.json`:
```json
{
    "OMDB_API_KEY": "your-api-key-here"
}
```

6. Run the Streamlit app:
```bash
cd src
streamlit run main.py
```

## Features

- Movie recommendations based on content similarity
- Real-time movie information from OMDB API
- Movie posters and plot summaries
- Progress tracking for recommendation loading
- Caching for faster subsequent searches

## Data Files
The preprocessing step will generate several pickle files that are necessary for the recommendation system to work:
- `cleaned.pkl`: Processed movie dataset
- `cosine_sim.pkl`: Pre-computed similarity matrix
- `tfidf_matrix.pkl`: TF-IDF vectors for movies

These files are not included in the repository due to their size but can be either:
1. Downloaded from the releases page, or
2. Generated using `preprocess.py`
