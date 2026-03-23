import streamlit as st
import pickle
import pandas as pd
import requests
import os
from recommender import create_model

# If files not exist → create them
if not os.path.exists("movies.pkl") or not os.path.exists("similarity.pkl"):
    create_model()


# -----------------------------------
# Load Model Safely
# -----------------------------------

try:
    movies = pickle.load(open('movies.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
except:
    if os.path.exists("movies.pkl"):
        os.remove("movies.pkl")
    if os.path.exists("similarity.pkl"):
        os.remove("similarity.pkl")

    st.error("Model files corrupted. Please reload app.")
    st.stop()


# -----------------------------------
# Page Config
# -----------------------------------

st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)


# -----------------------------------
# UI Styling
# -----------------------------------

st.markdown("""
<style>
body {
    background-color: #0E1117;
}
.stButton>button {
    background-color: #E50914;
    color: white;
    font-size:18px;
    border-radius:10px;
    padding:10px 25px;
}
.stButton>button:hover {
    background-color: #ff1e1e;
}
img {
    border-radius:12px;
}
.movie-title {
    text-align:center;
    font-weight:bold;
    font-size:16px;
    margin-top:5px;
}
.footer {
    text-align:center;
    margin-top:50px;
}
</style>
""", unsafe_allow_html=True)


# -----------------------------------
# Header
# -----------------------------------

st.markdown("""
<h1 style='text-align: center;'>🎬 Movie Recommendation System</h1>
<p style='text-align: center;'>Discover movies similar to your favorite ones</p>
""", unsafe_allow_html=True)


# -----------------------------------
# Genre Filter
# -----------------------------------

genre_list = [
    "Action","Adventure","Comedy","Drama","Romance",
    "Thriller","Fantasy","Animation","Horror","Sci-Fi"
]

selected_genre = st.selectbox("🎭 Filter movies by genre", genre_list)

filtered_movies = movies[movies['tags'].str.contains(selected_genre.lower(), na=False)]


# -----------------------------------
# Fetch Poster
# -----------------------------------

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=4872e75be5684ead687ca2ac52bf8dc3&language=en-US"
        data = requests.get(url).json()
        poster_path = data.get('poster_path')

        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/300x450?text=No+Poster"
    except:
        return "https://via.placeholder.com/300x450?text=Error"


# -----------------------------------
# Fetch Details
# -----------------------------------

def fetch_movie_details(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=4872e75be5684ead687ca2ac52bf8dc3&language=en-US"
        return requests.get(url).json()
    except:
        return {}


# -----------------------------------
# Trending Movies
# -----------------------------------

st.subheader("🔥 Trending Movies")

trending = movies.sample(5)
cols = st.columns(5)

for i in range(5):
    with cols[i]:
        movie_id = trending.iloc[i].movie_id
        st.image(fetch_poster(movie_id))
        st.markdown(f"**{trending.iloc[i].title}**")

        details = fetch_movie_details(movie_id)

        with st.expander("More Info"):
            st.write("⭐", details.get("vote_average"))
            st.write("📅", details.get("release_date"))
            st.write("📝", details.get("overview"))


# -----------------------------------
# Recommendation Function
# -----------------------------------

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]

    movie_list = sorted(list(enumerate(distances)),
                        reverse=True,
                        key=lambda x: x[1])[1:6]

    names = []
    posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        names.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))

    return names, posters


# -----------------------------------
# UI
# -----------------------------------

selected_movie = st.selectbox("🎥 Select Movie", filtered_movies['title'].values)

if st.button("Recommend"):
    names, posters = recommend(selected_movie)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(posters[i])
            st.markdown(f"**{names[i]}**")


# -----------------------------------
# Footer
# -----------------------------------

st.markdown("---")
st.markdown("<div class='footer'>Built with ❤️ using Streamlit</div>", unsafe_allow_html=True)
