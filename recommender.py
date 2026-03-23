import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def create_model():
    movies = pd.read_csv('data/tmdb_5000_movies.csv')
    credits = pd.read_csv('data/tmdb_5000_credits.csv')

    movies = movies.merge(credits, on='title')

    movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]
    movies.dropna(inplace=True)

    # Simple tag creation
    movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords']

    # Convert to string
    movies['tags'] = movies['tags'].astype(str)

    # Vectorization
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(movies['tags']).toarray()

    similarity = cosine_similarity(vectors)

    # Save files
    pickle.dump(movies[['movie_id','title','tags']], open('movies.pkl','wb'))
    pickle.dump(similarity, open('similarity.pkl','wb'))
