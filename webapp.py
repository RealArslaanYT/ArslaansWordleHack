from flask import Flask, render_template
import requests

app = Flask(__name__)
WORDLE_BASE_URL = "https://www.nytimes.com/svc/wordle/v2/DATE_PLACEHOLDER.json"


def get_wordle_solution(timestamp):
    try:
        wordleJson = requests.get(WORDLE_BASE_URL.replace("DATE_PLACEHOLDER", timestamp)).json()
    except requests.JSONDecodeError:
        wordleJson = {
            "status": "ERROR",
            "errors": [
                "Invalid date provided"
            ],
            "results": [],
        }
    try:
        return wordleJson["solution"].upper(), None
    except KeyError:
        return None, f'There was an error(s) getting the Wordle solution for {timestamp}: ' + ', '.join(wordleJson['errors'])


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/solution/<date>")
def view_solution(date):
    solution, error = get_wordle_solution(date)
    if solution is not None:
        return render_template("viewSolution.html", solution=solution, date=date)
    else:
        return render_template("viewSolution.html", error=error)


app.run('0.0.0.0', 80)
