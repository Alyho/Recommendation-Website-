#Routes 
from flask import Flask
from flask import render_template
from flask import request
from Model.TestMethods import NumberGuessing

app = Flask(__name__)

NumberGuess = NumberGuessing()
#tries = 7

@app.route("/")
def index():
    return render_template('index.html', content="Try your luck!")

@app.route("/guess", methods=['POST', 'GET'])
def guess_number():
    if request.method == 'POST':
        #global tries
        value = NumberGuess.guess(int(request.form['guess']))
        if value == -999:
            message = "You ran out of guesses."
        elif value == 1:
            #tries -= 1
            message = "Your guess is too large. Try again." #You have " + str(tries) + " left."

        elif value == -1 :
            #tries -= 1
            message = "Your guess is too small. Try again." #You have " + str(tries) + " left."
        else:
            message = "Correct!"

        return render_template('index.html', content=message)


if __name__ == "__main__":
    app.run("0.0.0.0", 4096)