# 🎬 Movie Recommendation System

A modern movie recommendation web application built using **Python, Machine Learning, and Streamlit**.

The app suggests similar movies based on content using **cosine similarity** and displays movie posters and details using the **TMDB API**.

---

## 📱 App Preview

This application provides a clean UI where users can:

- Select a movie
- Get similar movie recommendations
- View movie posters
- Filter by genres
- Explore trending movies

---

## 🚀 Tech Stack

### 🧠 Machine Learning
- Python
- Pandas
- Scikit-learn
- CountVectorizer
- Cosine Similarity

### 🎨 Frontend
- Streamlit
- Custom CSS

### 🌐 API
- TMDB API (for posters & movie details)

---

## ✨ Features

### 🎥 Movie Recommendation
- Suggests 5 similar movies based on selected movie
- Uses content-based filtering

### 🎭 Genre Filtering
- Filter movies by genres like Action, Comedy, Drama, etc.

### 🖼 Movie Posters
- Fetches posters dynamically using TMDB API

### 🔥 Trending Movies
- Displays random trending movies on homepage

### 📄 Movie Details
- Shows:
  - Rating ⭐
  - Release Date 📅
  - Runtime ⏱
  - Overview 📝

---

## 🧠 How It Works

1. Movie data is preprocessed and combined into a single feature column (`tags`)
2. Text is converted into vectors using **CountVectorizer**
3. Similarity between movies is calculated using **Cosine Similarity**
4. Top 5 similar movies are recommended

---

## 📂 Project Structure
movie-recommendation-system
│
├── app.py # Streamlit app
├── recommender.py # ML logic
├── README.md
├── requirements.txt
│
├── notebooks/
│ └── movie_recommendation.ipynb



---

## 🗄 Dataset

Dataset used:

👉 https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/ruchira-patil/movie-recommendation-system.git


Go to project folder:

cd movie-recommendation-system

Install dependencies:

pip install -r requirements.txt

Run the app:

streamlit run app.py

🔑 API Setup

Get your API key from:

👉 https://www.themoviedb.org/

Replace in code:
api_key = "YOUR_API_KEY"


🧠 Learning Outcomes

Built a recommendation system using ML

Learned feature engineering and vectorization

Worked with real-world API integration

Built UI using Streamlit

Understood cosine similarity

🚀 Future Improvements

Add user login system

Add collaborative filtering

Add search functionality

Improve UI/UX

Deploy on cloud

👨‍💻 Author

Ruchira Patil

⭐ Support

If you like this project, give it a ⭐ on GitHub!
