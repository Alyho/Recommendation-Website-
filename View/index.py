#Routes
import time

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from Model import TestMethods
from Model.Model import Model

app = Flask(__name__)

tries = 7

# NumberGuess = NumberGuessing()
GetMovies = TestMethods.getMovieRatingsThings()

@app.route("/")
def index():
    list = GetMovies
    #NumberGuess.reset()
    return render_template('index.html', data1 = list[0], data2 = list[1])

@app.route("/recc", methods=['POST', 'GET'])
def guess_number():
    if m.loaded:
        list = GetMovies
        if request.method == 'POST':
            startime = time.time()
            userfeatures = TestMethods.wrapMovies(request.form['gender'], request.form['age'], request.form['occ'],
                                            request.form['zip'])
            print(userfeatures)
            ratings_in_order = {}
            for i in range(3952):
                ratings_in_order[i] = m.predict(userfeatures, i)

            actual_movie_ratings = []
            movie_raitngs = []
            # for w in sorted(ratings_in_order.)
            for w in sorted(ratings_in_order, key=ratings_in_order.get, reverse=True):
                actual_movie_ratings.append(m.predict(userfeatures, w))
                movie_raitngs.append(m.movie_number_dict.get(w))

            movies = movie_raitngs[:10]
            j = []
            for i in range(len(movies)):
                j .append( str(movie_raitngs[i]) + ":" + str(actual_movie_ratings[i]) + ",")
            j.append(str(time.time()-startime))
            print(movies)
            movies = j
            # print(m.predict(userfeatures, movies[0]))

            return render_template('index.html', content=movies, data1 = list[0], data2 = list[1])

@app.route("/reset", methods=['POST', 'GET'])
def reset_number():
    list = GetMovies
    if request.method == "POST":
        #NumberGuess.reset()
        return render_template('index.html', data1 = list[0], data2 = list[1])

if __name__ == "__main__":
    import threading
    m = Model()
    t = threading.Thread(target=m.load_model_from_file())
    t.start()
    app.run("0.0.0.0", 4096)