#Routes 
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from Model import TestMethods
from Model.TestMethods import NumberGuessing

app = Flask(__name__)

tries = 7

NumberGuess = NumberGuessing()
GetMovies = TestMethods.getMovieRatingsThings()

@app.route("/")
def index():
    list = GetMovies
    #NumberGuess.reset()
    return render_template('index.html', data1 = list[0], data2 = list[1])

@app.route("/recc", methods=['POST', 'GET'])
def guess_number():
    list = GetMovies
    if request.method == 'POST':
        movies = TestMethods.getRecommendedMovies(request.form['gender'], request.form['age'], request.form['occ'], 
                                             request.form['zip'])
        #if value == -999 or NumberGuess.tries == 0:
         #   return redirect("/")

        #elif value == 1:
         #   message = "Your guess is too large. Try again. You have " + str(NumberGuess.tries) + " left."

        #elif value == -1 :
         #   message = "Your guess is too small. Try again. You have " + str(NumberGuess.tries) + " left."
        #else:
         #   message = "Correct!"

        return render_template('index.html', content=movies, data1 = list[0], data2 = list[1])

@app.route("/reset", methods=['POST', 'GET'])
def reset_number():
    list = GetMovies
    if request.method == "POST":
        #NumberGuess.reset()
        return render_template('index.html', data1 = list[0], data2 = list[1])

if __name__ == "__main__":
    app.run("0.0.0.0", 4096)