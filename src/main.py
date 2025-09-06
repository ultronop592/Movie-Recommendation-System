import json
import streamlit as st
from recommend import movie, recommend_movies
from omdb_utils import get_movie_details_single

config = json.load(open("config.json"))

# OMDB api key
OMDB_API_KEY = config["OMDB_API_KEY"]

st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 Movie Recommender")

# Using 'title' instead of 'song' now
movie_list = sorted(movie['title'].dropna().unique())
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

if st.button("Show Recommendation"):
    # First find recommendations
    with st.spinner("🔍 Finding similar movies..."):
        recommendations = recommend_movies(selected_movie)
        
        if recommendations is None or recommendations.empty:
            st.warning("⚠️ No recommendations found. Please try another movie.")
        else:
            movie_titles = recommendations['title'].tolist()
            
            # Show progress for movie details fetching
            progress_text = "🎬 Getting movie details..."
            my_bar = st.progress(0, text=progress_text)
            
            # Initialize empty details dictionary
            movie_details = {}
            
            # Process movies with progress bar
            for idx, title in enumerate(movie_titles):
                # Update progress
                progress = (idx + 1) / len(movie_titles)
                my_bar.progress(progress, text=f"{progress_text} ({idx + 1}/{len(movie_titles)})")
                
                # Get movie details
                result = get_movie_details_single(title, OMDB_API_KEY)
                movie_details[title] = {
                    'plot': result[1],
                    'poster': result[2],
                    'year': result[3],
                    'rating': result[4]
                }
            
            # Clear progress bar
            my_bar.empty()
            
            st.success("✅ Here are your movie recommendations!")
            
            for i, row in recommendations.iterrows():
                title = row['title']
                movie_info = movie_details[title]
                
                st.container()
                col1, col2 = st.columns([1,3])
                
                with col1:
                    if movie_info['poster'] != "N/A":
                        st.image(movie_info['poster'], width=150)
                    else:
                        st.markdown(
                            """
                            <div style="width:150px;height:225px;background:#f0f0f0;
                            display:flex;align-items:center;justify-content:center;border-radius:10px">
                                <span style="color:#666">No image available</span>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                
                with col2:
                    title_text = f"### {title}"
                    if movie_info['year'] != 'N/A':
                        title_text += f" ({movie_info['year']})"
                    if movie_info['rating'] != 'N/A':
                        title_text += f" ⭐ {movie_info['rating']}/10"
                    st.markdown(title_text)
                    
                    if movie_info['plot'] != 'N/A':
                        st.markdown(f"**Plot:** {movie_info['plot']}")
                    else:
                        st.markdown("*Plot not available for this movie*")
                
                st.markdown("---")
