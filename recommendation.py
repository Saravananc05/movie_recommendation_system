import pandas as pd
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load datasets
movies = pd.read_csv("tmdb_5000_movies.csv")
credits = pd.read_csv("tmdb_5000_credits.csv")
details = pd.read_csv("movie_details.csv")

details.columns = details.columns.str.strip()

# Merge datasets
movies = movies.merge(credits, on="title")

movies = movies.merge(
    details,
    left_on="id",
    right_on="id",
    how="left"
)

# Keep only required columns
movies = movies[
    [
        'movie_id',
        'title',
        'overview',
        'genres',
        'keywords',
        'cast',
        'crew',
        'poster_url',
        'rating',
        'year'
    ]
]


def convert(text):
    result = []

    try:
        for i in ast.literal_eval(text):
            result.append(i['name'])
    except:
        pass

    return result


def fetch_cast(text):
    result = []

    try:
        counter = 0

        for i in ast.literal_eval(text):

            if counter < 3:
                result.append(i['name'])
                counter += 1
            else:
                break

    except:
        pass

    return result


def fetch_director(text):
    result = []

    try:
        for i in ast.literal_eval(text):

            if i['job'] == 'Director':
                result.append(i['name'])
                break

    except:
        pass

    return result


# Remove missing values
movies.dropna(inplace=True)

# Feature extraction
movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
movies['cast'] = movies['cast'].apply(fetch_cast)
movies['crew'] = movies['crew'].apply(fetch_director)

movies['overview'] = movies['overview'].apply(
    lambda x: x.split()
)

movies['genres'] = movies['genres'].apply(
    lambda x: [i.replace(" ", "") for i in x]
)

movies['keywords'] = movies['keywords'].apply(
    lambda x: [i.replace(" ", "") for i in x]
)

movies['cast'] = movies['cast'].apply(
    lambda x: [i.replace(" ", "") for i in x]
)

movies['crew'] = movies['crew'].apply(
    lambda x: [i.replace(" ", "") for i in x]
)

movies['tags'] = (
    movies['overview']
    + movies['genres']
    + movies['keywords']
    + movies['cast']
    + movies['crew']
)

# Final dataframe
new_df = movies[
    [
        'movie_id',
        'title',
        'tags',
        'poster_url',
        'rating',
        'year'
    ]
].copy()

new_df['tags'] = new_df['tags'].apply(
    lambda x: " ".join(x)
)

# Reduced memory usage
cv = CountVectorizer(
    max_features=1500,
    stop_words='english'
)

vectors = cv.fit_transform(new_df['tags'])


def get_movie_details(movie_name):

    matches = movies[
        movies['title'].str.lower().str.contains(
            movie_name.lower(),
            na=False
        )
    ]

    if matches.empty:
        return None

    movie = matches.iloc[0]

    return {
        "title": movie["title"],
        "rating": movie["rating"],
        "year": int(movie["year"]) if pd.notna(movie["year"]) else "N/A",
        "poster_url": movie["poster_url"],
        "imdb_url": f"https://www.imdb.com/find/?q={movie['title'].replace(' ','+')}"
    }


def recommend(movie_name):

    movie_name = movie_name.lower()

    matches = new_df[
        new_df['title'].str.lower().str.contains(
            movie_name,
            na=False
        )
    ]

    if matches.empty:
        return []

    movie = matches.iloc[0]['title']

    movie_index = new_df[
        new_df['title'] == movie
    ].index[0]

    # Memory-efficient similarity calculation
    movie_vector = vectors[movie_index]

    distances = cosine_similarity(
        movie_vector,
        vectors
    ).flatten()

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:11]

    recommendations = []

    for i in movie_list:

        row = new_df.iloc[i[0]]

        recommendations.append({
            "title": row["title"],
            "rating": row["rating"],
            "year": int(row["year"]) if pd.notna(row["year"]) else "N/A",
            "poster_url": row["poster_url"],
            "imdb_url": f"https://www.imdb.com/find/?q={row['title'].replace(' ','+')}"
        })

    return recommendations