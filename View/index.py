#Routes
import time
import random

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

def resetList():
    list = GetMovies
    list1 = random.sample(list[0], 5)
    list2 = random.sample(list[1], 10)
    return list2 + list1

@app.route("/")
def index():
    #NumberGuess.reset()
    global movieList 
    movieList = resetList()
    return render_template('index.html', data = movieList)

@app.route("/lr", methods=['POST', 'GET'])
def guess_number():
    global movieList
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

            return render_template('index.html', content=movies, data = movieList)

@app.route("/nn", methods=['POST', 'GET'])
def nueral_network():
    global movieList
    ratingsList = []
    if request.method == "POST":
        #NumberGuess.reset()
        for i in range(len(movieList)):
            rating = [movieList[i], request.form['stars' + str(i + 1)]]
            ratingsList.append(rating)

        #Neural Network Call here
        #recommendedMovies = neuralnetwork(ratingsList)

        return render_template('index.html', data = movieList, recc = ratingsList)

@app.route("/reset", methods=['POST', 'GET'])
def reset_number():
    global movieList
    if request.method == "POST":
        #NumberGuess.reset()
        return render_template('index.html', data = movieList)

@app.route("/reset2", methods=['POST', 'GET'])
def reset_movies():
    global movieList
    if request.method == "POST":
        movieList = resetList()
        #NumberGuess.reset()
        return render_template('index.html', data = movieList)

if __name__ == "__main__":
    import threading
    m = Model()
    t = threading.Thread(target=m.load_model_from_file())
    t.start()
    app.run("0.0.0.0", 4096)