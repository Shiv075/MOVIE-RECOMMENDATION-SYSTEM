import streamlit as st
import pandas as pd
import pickle
import bz2
import requests

# TMDB API Key
API_KEY = '8265bd1679663a7ea12ac168da84d2e8'


# Fetch movie poster from TMDB
def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US'
    )
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


# Fetch movie trailer (YouTube) from TMDB
def fetch_trailer(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={API_KEY}&language=en-US'
    )
    data = response.json()
    videos = data.get('results', [])
    for video in videos:
        if video['type'] == 'Trailer' and video['site'] == 'YouTube':
            return f"https://www.youtube.com/watch?v={video['key']}"
    return None  # No trailer found


# Recommend similar movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    recommended_trailers = []
    recommended_movie_links = []  # Placeholder links to full movie (e.g., JustWatch, etc.)

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
        recommended_trailers.append(fetch_trailer(movie_id))
        # Example placeholder link, in practice, use an API like JustWatch to get the real link
        recommended_movie_links.append(
            f"https://www.justwatch.com/us/movie/{movies.iloc[i[0]].title.replace(' ', '-').lower()}")

    return recommended_movies, recommended_posters, recommended_trailers, recommended_movie_links


# Load data
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
with bz2.BZ2File('similarity.pkl.bz2', 'rb') as f:
    similarity = pickle.load(f)


# App title
st.markdown(
    "<h1 style='text-align: center; color: #FF4B4B;'>🎬 Movie Recommendation System</h1><hr>",
    unsafe_allow_html=True
)

# Movie selection
selected_movie_name = st.selectbox('Choose a movie you like:', movies['title'].values)

# Show recommendations
if st.button('Show Recommendations'):
    names, posters, trailers, full_movie_links = recommend(selected_movie_name)

    # Custom CSS for updated button styling
    st.markdown("""
        <style>
        .movie-card {
            border: 2px solid #f0f0f0;
            border-radius: 15px;
            padding: 10px;
            margin: 10px auto;
            text-align: center;
            background-color: #fff5f5;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }
        .movie-card:hover {
            transform: scale(1.05);
        }
        .movie-title {
            font-weight: bold;
            font-size: 16px;
            margin-top: 10px;
            color: #333;
        }
        .movie-img {
            width: 200px;
            height: 200px;
            object-fit: cover;
            border-radius: 10px;
        }
        .watch-button {
            color: blue;
            font-weight: bold;
            text-decoration: none;
            margin-top: 10px;
            font-size: 14px;
        }
        .trailer-button {
            color: blue;
            font-weight: bold;
            text-decoration: none;
            margin-top: 10px;
            font-size: 14px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("### ✨ Recommended For You: ✨")
    cols = st.columns(5)

    for idx in range(5):
        trailer_link = trailers[idx] if trailers[idx] else "#"
        full_movie_link = full_movie_links[idx]

        with cols[idx]:
            st.markdown(f"""
                <div class="movie-card">
                    <a href="{trailer_link}" target="_blank" class="trailer-button">🎥 Watch Trailer</a><br>
                    <img src="{posters[idx]}" class="movie-img">
                    <div class="movie-title">{names[idx]}</div>
                    <a href="{full_movie_link}" target="_blank" class="watch-button">🍿 Watch Full Movie</a>
                </div>
            """, unsafe_allow_html=True)
try:

# Footer
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
         "<p style='text-align: center; font-size: 14px;'>❤❤ copyright by @ HRITIK KUMAR AND SHIVRAJ SINGH ❤❤</p>",
        unsafe_allow_html=True
         )
except Exception as e:
    print('ERROR MESSAGES',e)