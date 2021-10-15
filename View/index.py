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
    NumberGuess.reset()
    return render_template('index.html', content="Try your luck!", data1 = list[0], data2 = list[1])

@app.route("/guess", methods=['POST', 'GET'])
def guess_number():
    list = GetMovies
    if request.method == 'POST':
        value = NumberGuess.guess(int(request.form['guess']))
        if value == -999 or NumberGuess.tries == 0:
            return redirect("/")

        elif value == 1:
            message = "Your guess is too large. Try again. You have " + str(NumberGuess.tries) + " left."

        elif value == -1 :
            message = "Your guess is too small. Try again. You have " + str(NumberGuess.tries) + " left."
        else:
            message = "Correct!"

        return render_template('index.html', content=message, data1 = list[0], data2 = list[1])

@app.route("/reset", methods=['POST', 'GET'])
def reset_number():
    if request.method == "POST":
        NumberGuess.reset()
        return render_template('index.html', content="New Game beginning!")

if __name__ == "__main__":
    app.run("0.0.0.0", 4096)