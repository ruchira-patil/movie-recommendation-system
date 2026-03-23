import pandas as pd
import pickle
import requests
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def download_csv(url, filename):
    if not os.path.exists(filename):
        r = requests.get(url)
        with open(filename, "wb") as f:
            f.write(r.content)


def create_model():

    # Download datasets automatically
    download_csv(
        "https://raw.githubusercontent.com/ashishpatel26/ML-Datasets/main/tmdb_5000_movies.csv",
        "tmdb_5000_movies.csv"
    )

    download_csv(
        "https://raw.githubusercontent.com/ashishpatel26/ML-Datasets/main/tmdb_5000_credits.csv",
        "tmdb_5000_credits.csv"
    )

    movies = pd.read_csv('tmdb_5000_movies.csv')
    credits = pd.read_csv('tmdb_5000_credits.csv')

    movies = movies.merge(credits, on='title')

    movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]
    movies.dropna(inplace=True)

    movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords']
    movies['tags'] = movies['tags'].astype(str)

    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(movies['tags']).toarray()

    similarity = cosine_similarity(vectors)

    pickle.dump(movies[['movie_id','title','tags']], open('movies.pkl','wb'))
    pickle.dump(similarity, open('similarity.pkl','wb'))
