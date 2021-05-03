import csv
from collections import namedtuple

from flask import Flask, render_template

app = Flask(__name__)

Quizset = namedtuple('Quizset', 'filename title')


@app.route("/")
def index():
    with open('quiz/index.txt', newline='', encoding='utf-8-sig') as f:
        rows = csv.reader(f, delimiter='\t')
        sets = [Quizset(*row) for row in rows]

    return render_template('index.html', title='Quiz Web', sets=sets)


if __name__ == "__main__":
    app.run()
