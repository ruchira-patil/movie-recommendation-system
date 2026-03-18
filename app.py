import streamlit as st
import pickle
import pandas as pd
import requests
import gdown
import os

# Download files if not present
if not os.path.exists("movies.pkl"):
    gdown.download("https://drive.google.com/uc?id=1fPB8mkl4xkbdQDg-itIZJ4DfzqLhhFSq", "movies.pkl", quiet=False)

if not os.path.exists("similarity.pkl"):
    gdown.download("https://drive.google.com/uc?id=1AckfThonxQe10ZRkwlaKWydjYXIeaSkz", "similarity.pkl", quiet=False)

# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)


# -----------------------------------
# Custom CSS Styling
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
    color: white;
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
    font-size:14px;
}

.poster {
    transition: transform 0.3s;
}

.poster:hover {
    transform: scale(1.08);
}
            
</style>
""", unsafe_allow_html=True)


# -----------------------------------
# Header
# -----------------------------------

st.markdown(
"""
<h1 style='text-align: center;'>🎬 Movie Recommendation System</h1>
<p style='text-align: center; font-size:18px;'>Discover movies similar to your favorite ones</p>
""",
unsafe_allow_html=True
)


# -----------------------------------
# Load Saved Model Files
# -----------------------------------

movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))


# -----------------------------------
# Genre Filter
# -----------------------------------

genre_list = [
    "Action","Adventure","Comedy","Drama","Romance",
    "Thriller","Fantasy","Animation","Horror","Sci-Fi"
]

selected_genre = st.selectbox("🎭 Filter movies by genre (optional)", genre_list)

filtered_movies = movies[movies['tags'].str.contains(selected_genre.lower(), na=False)]

# -----------------------------------
# Fetch Movie Poster from TMDB
# -----------------------------------

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=4872e75be5684ead687ca2ac52bf8dc3&language=en-US"
        response = requests.get(url)
        data = response.json()

        poster_path = data.get('poster_path')

        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/300x450?text=No+Poster"

    except:
        return "https://via.placeholder.com/300x450?text=No+Poster"


def fetch_movie_details(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=4872e75be5684ead687ca2ac52bf8dc3&language=en-US"
        response = requests.get(url)
        data = response.json()
        return data
    except:
        return {}

st.subheader("🔥 Trending Movies")

trending = movies.sample(5)

cols = st.columns(5)

for i in range(5):
    with cols[i]:

        movie_id = trending.iloc[i].movie_id
        poster = fetch_poster(movie_id)
        title = trending.iloc[i].title

        st.image(poster)
        st.markdown(
            f"<div class='movie-title'>{title}</div>",
            unsafe_allow_html=True
        )

        details = fetch_movie_details(movie_id)

        with st.expander("More Info"):
            st.write("⭐ Rating:", details.get("vote_average", "N/A"))
            st.write("📅 Release:", details.get("release_date", "N/A"))
            st.write("⏱ Runtime:", details.get("runtime", "N/A"), "minutes")
            st.write("📝 Overview:", details.get("overview", "No description available"))


# -----------------------------------
# Recommendation Function
# -----------------------------------

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters


# -----------------------------------
# Movie Selection UI
# -----------------------------------

selected_movie = st.selectbox(
    "🎥 Choose a movie",
    filtered_movies['title'].values
)


# -----------------------------------
# Recommendation Button
# -----------------------------------

if st.button("Recommend"):

    with st.spinner("Finding similar movies..."):

        names, posters = recommend(selected_movie)

        cols = st.columns(5)

        for i in range(5):
            with cols[i]:
                st.image(posters[i])
                st.markdown(
                    f"<div class='movie-title'>{names[i]}</div>",
                    unsafe_allow_html=True
                )


# -----------------------------------
# Footer
# -----------------------------------

st.markdown("---")

st.markdown(
"""
<div class="footer">
Built with ❤️ using Python, Streamlit & Machine Learning
</div>
""",
unsafe_allow_html=True
)
