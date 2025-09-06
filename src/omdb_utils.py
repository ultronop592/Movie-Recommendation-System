import requests
import logging
import json
import os
from concurrent.futures import ThreadPoolExecutor
import urllib.parse
from pathlib import Path

# Create a cache directory if it doesn't exist
CACHE_DIR = Path(__file__).parent / "movie_cache"
CACHE_DIR.mkdir(exist_ok=True)

def load_cache():
    """Load the movie cache from disk"""
    cache_file = CACHE_DIR / "movie_cache.json"
    if cache_file.exists():
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_cache(cache):
    """Save the movie cache to disk"""
    cache_file = CACHE_DIR / "movie_cache.json"
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(cache, f, indent=2)

# Load the cache at module level
MOVIE_CACHE = load_cache()

def clean_movie_title(title):
    """Clean movie title for API request"""
    # Remove any year in parentheses and clean up
    title = title.split('(')[0].strip()
    # Remove special characters but keep spaces
    title = ''.join(c for c in title if c.isalnum() or c.isspace())
    return urllib.parse.quote(title)

def get_movie_details_single(title, api_key):
    """
    Get movie details from OMDB API for a single movie
    Returns: (title, plot, poster_url)
    """
    global MOVIE_CACHE
    
    # Check cache first
    if title in MOVIE_CACHE:
        return (title, 
                MOVIE_CACHE[title]['plot'],
                MOVIE_CACHE[title]['poster'],
                MOVIE_CACHE[title]['year'],
                MOVIE_CACHE[title]['rating'])
    
    try:
        clean_title = clean_movie_title(title)
        # First try exact search
        url = f"http://www.omdbapi.com/?t={clean_title}&apikey={api_key}"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        # If exact search fails, try search endpoint
        if data.get('Response') != 'True':
            search_url = f"http://www.omdbapi.com/?s={clean_title}&apikey={api_key}"
            search_response = requests.get(search_url, timeout=5)
            search_data = search_response.json()
            
            if search_data.get('Response') == 'True' and search_data.get('Search'):
                # Get the first result's IMDB ID
                imdb_id = search_data['Search'][0]['imdbID']
                # Get full details using IMDB ID
                url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={api_key}"
                response = requests.get(url, timeout=5)
                data = response.json()
        
        if response.status_code == 200 and data.get('Response') == 'True':
            # Cache the results
            MOVIE_CACHE[title] = {
                'plot': data.get('Plot', 'N/A'),
                'poster': data.get('Poster', 'N/A'),
                'year': data.get('Year', 'N/A'),
                'rating': data.get('imdbRating', 'N/A')
            }
            save_cache(MOVIE_CACHE)
            
            return (title, 
                   MOVIE_CACHE[title]['plot'],
                   MOVIE_CACHE[title]['poster'],
                   MOVIE_CACHE[title]['year'],
                   MOVIE_CACHE[title]['rating'])
            
    except Exception as e:
        logging.error(f"❌ Error fetching details for '{title}': {str(e)}")
    
    # If anything fails, return N/A and don't cache
    return (title, 'N/A', 'N/A', 'N/A', 'N/A')

def get_movie_details(titles, api_key):
    """
    Get movie details from OMDB API for multiple movies in parallel
    Returns: Dictionary of movie details
    """
    with ThreadPoolExecutor(max_workers=5) as executor:
        # Create tasks for each movie
        futures = [executor.submit(get_movie_details_single, title, api_key) 
                  for title in titles]
        
        # Collect results
        results = {}
        for future in futures:
            title, plot, poster, year, rating = future.result()
            results[title] = {
                'plot': plot,
                'poster': poster,
                'year': year,
                'rating': rating
            }
        
        return results
