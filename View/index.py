#Routes 
from flask import Flask
from flask import render_template
from flask import request
from Model.TestMethods import NumberGuessing

app = Flask(__name__)

tries = 7

NumberGuess = NumberGuessing()
@app.route("/")
def index():
    NumberGuess.reset()
    return render_template('index.html', content="Try your luck!")

@app.route("/guess", methods=['POST', 'GET'])
def guess_number():
    if request.method == 'POST':
        value = NumberGuess.guess(int(request.form['guess']))
        if value == -999:
            message = "You ran out of guesses."

        elif value == 1:
            message = "Your guess is too large. Try again. You have " + str(NumberGuess.tries) + " left."

        elif value == -1 :
            message = "Your guess is too small. Try again. You have " + str(NumberGuess.tries) + " left."
        else:
            message = "Correct!"

        return render_template('index.html', content=message)


if __name__ == "__main__":
    app.run("0.0.0.0", 4096)