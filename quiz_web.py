import csv
from collections import namedtuple
from pathlib import Path

from flask import Flask, render_template

app = Flask(__name__)

QuizSet = namedtuple('QuizSet', 'filename title description')
QuizData = namedtuple('QuizData', 'question comment choices')
quiz_dir = Path(__file__).parent.resolve() / 'quiz'


def get_qsets():
    """クイズ集のリストを取得する
    """
    with open(quiz_dir / 'index.tsv', newline='', encoding='utf-8-sig') as f:
        rows = csv.reader(f, delimiter='\t')
        qsets = [QuizSet(*row) for row in rows]
    return qsets


def get_qset_data(filename):
    """クイズ集のデータを取得する
    """
    with open(quiz_dir / filename, newline='', encoding='utf-8-sig') as f:
        rows = csv.reader(f, delimiter='\t')
        qset_data = [QuizData(row[0], row[1], row[2:]) for row in rows]
    return qset_data


@app.route('/')
def index():
    """インデックスページを返す
    """
    title = 'Quiz Web - Index'
    return render_template('index.html', title=title, qsets=get_qsets())


@app.route('/qset/<int:qset_idx>')
def quiz_set(qset_idx=0):
    """クイズ集のクイズ一覧を返す
    """
    qset = get_qsets()[qset_idx]
    qset_data = get_qset_data(qset.filename)
    title = f'Quiz Web - {qset.title}'
    return render_template(
        'quiz_set.html', title=title,
        qset_idx=qset_idx, qset=qset, qset_data=qset_data)


if __name__ == "__main__":
    app.run(debug=True)
