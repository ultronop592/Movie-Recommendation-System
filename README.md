# 🎬 Movie Recommendation System

A content-based movie recommendation system built with Python, Streamlit, and OMDB API integration. Get personalized movie recommendations based on movie similarity using advanced NLP techniques.

## 🌟 Features

- **Content-based Recommendations**: Uses TF-IDF and cosine similarity for accurate movie suggestions
- **Real-time Movie Data**: Fetches movie details, posters, and ratings from OMDB API
- **Interactive Web Interface**: Built with Streamlit for a smooth user experience
- **Smart Caching**: Optimized performance with intelligent caching system
- **4000+ Movies**: Extensive movie database for diverse recommendations

## 🚀 Live Demo

[🔗 Try the live app here](your-deployed-app-url) *(Will be updated after deployment)*

## 📁 Project Structure

```
Movie-Recommendation-System/
├── src/
│   ├── main.py              # Streamlit web application
│   ├── recommend.py         # Recommendation engine
│   ├── preprocess.py        # Data preprocessing
│   ├── omdb_utils.py        # OMDB API utilities
│   ├── config.json          # Configuration file
│   ├── movies.csv           # Movie dataset
│   ├── cleaned.parquet      # Processed movie data
│   ├── cosine_sim.npz       # Similarity matrix
│   └── tfidf_matrix.npz     # TF-IDF vectors
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🛠️ Pre-trained Model Files

The system requires preprocessed data files for optimal performance:

**Included in repository:**
- `movies.csv`: Raw movie dataset
- `config.json`: API configuration

**Generated automatically (excluded from git due to size):**
- `cleaned.parquet`: Processed movie dataset
- `cosine_sim.npz`: Pre-computed similarity matrix  
- `tfidf_matrix.npz`: TF-IDF vectors for movies

**Options to get the data files:**
1. **Run preprocessing locally** (recommended for development)
2. **Download from releases** (for quick setup)
3. **Use deployment script** (for production)

## 🚀 Quick Start

### Local Development

1. **Clone the repository:**
```bash
git clone https://github.com/ultronop592/Movie-Recommendation-System.git
cd Movie-Recommendation-System
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure OMDB API:**
   - Get a free API key from [omdbapi.com](http://www.omdbapi.com/)
   - Update `src/config.json` with your API key

4. **Generate data files:**
```bash
cd src
python preprocess.py
```

5. **Run the application:**
```bash
streamlit run src/main.py
```

6. **Open your browser** and go to `http://localhost:8501`

## 🌐 Deployment Options

### Option 1: Streamlit Cloud (Recommended - Free)

1. **Push to GitHub** (if not already done)
2. **Visit** [share.streamlit.io](https://share.streamlit.io)
3. **Connect your GitHub account**
4. **Deploy** by selecting your repository
5. **Set main file path** to `src/main.py`
6. **Add secrets** in Streamlit Cloud settings:
   ```
   OMDB_API_KEY = "your-api-key-here"
   ```

### Option 2: Heroku

1. **Create** `Procfile` in root directory:
   ```
   web: streamlit run src/main.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Create** `setup.sh` for Heroku:
   ```bash
   mkdir -p ~/.streamlit/
   echo "\
   [server]\n\
   headless = true\n\
   port = $PORT\n\
   enableCORS = false\n\
   \n\
   " > ~/.streamlit/config.toml
   ```

3. **Deploy to Heroku:**
   ```bash
   heroku create your-app-name
   git push heroku main
   heroku config:set OMDB_API_KEY=your-api-key
   ```

### Option 3: Railway

1. **Visit** [railway.app](https://railway.app)
2. **Connect GitHub** and select your repository
3. **Add environment variables:**
   - `OMDB_API_KEY`: Your OMDB API key
4. **Deploy automatically**

## 🔧 Configuration

### Environment Variables

For deployment, set these environment variables:

- `OMDB_API_KEY`: Your OMDB API key

### API Key Setup

1. Visit [omdbapi.com](http://www.omdbapi.com/)
2. Sign up for a free account
3. Get your API key
4. Add it to `src/config.json` or as an environment variable

## 🛠️ Troubleshooting

**Common Issues:**

1. **Missing data files:**
   - Run `python src/preprocess.py` to generate them
   
2. **Import errors:**
   - Install dependencies: `pip install -r requirements.txt`
   
3. **API errors:**
   - Check your OMDB API key in `src/config.json`
   
4. **Memory issues:**
   - The system works with large datasets but may require sufficient RAM

## 📊 Technical Details

- **Algorithm**: Content-based filtering using TF-IDF and cosine similarity
- **Frontend**: Streamlit web framework
- **Data**: 4000+ movies with metadata
- **API**: OMDB for real-time movie information
- **Storage**: Efficient sparse matrix storage for similarity calculations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- OMDB API for movie data
- The Movie Database (TMDb) for the original dataset
- Streamlit for the amazing web framework
