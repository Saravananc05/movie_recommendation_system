from flask import Flask, render_template, request
from recommendation import recommend, get_movie_details

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    recommendations = []
    movie_details = None

    if request.method == "POST":

        movie_name = request.form["movie"]

        movie_details = get_movie_details(movie_name)

        recommendations = recommend(movie_name)

    return render_template(
        "index.html",
        recommendations=recommendations,
        movie_details=movie_details
    )

if __name__ == "__main__":
    app.run(debug=True)