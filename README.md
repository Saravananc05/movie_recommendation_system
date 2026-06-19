Movie Recommendation System

A Flask-based Movie Recommendation System that recommends similar movies using Content-Based Filtering and the TMDB 5000 Dataset.

Features

- Movie search
- Content-based movie recommendations
- Movie posters
- IMDb links
- Movie ratings
- Release year display
- Responsive and attractive UI

Technologies Used

- Python
- Flask
- Pandas
- Scikit-learn
- HTML
- CSS

Dataset

- TMDB 5000 Movies Dataset
- TMDB 5000 Credits Dataset

How to Run

1. Install dependencies

pip install flask pandas scikit-learn

2. Run the application

python app.py

3. Open in browser

http://127.0.0.1:5000

Project Structure

movie_recommendation/
│
├── app.py
├── recommendation.py
├── tmdb_5000_movies.csv
├── tmdb_5000_credits.csv
├── movie_details.csv
│
├── templates/
│   └── index.html
│
└── static/
    └── style.css
