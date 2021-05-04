import csv
import random
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
def index_page():
    """インデックスページを返す
    """
    title = 'Quiz Web - クイズ集一覧'
    return render_template('index.html', title=title, qsets=get_qsets())


@app.route('/qset/<int:qset_idx>')
def qset_page(qset_idx):
    """クイズ集のクイズ一覧ページを返す
    """
    # インデックスを元にクイズ集とそのデータを取得する
    qset = get_qsets()[qset_idx]
    qset_data = get_qset_data(qset.filename)

    # ページを返す
    title = f'Quiz Web - {qset.title}'
    return render_template(
        'qset.html', title=title,
        qset_idx=qset_idx, qset=qset, qset_data=qset_data)


@app.route('/q/<int:qset_idx>/<quiz_idx>')
def quiz_page(qset_idx, quiz_idx):
    """クイズページを返す
    """
    # インデックスを元にクイズ集とそのデータを取得する
    qset = get_qsets()[qset_idx]
    qset_data = get_qset_data(qset.filename)

    # quiz_idx が -1 ならランダムにする
    quiz_idx = int(quiz_idx)
    if quiz_idx < 0:
        quiz_idx = random.randint(0, len(qset_data) - 1)

    # TODO: 選択肢をランダムに並べ替え、正解のインデックスをテンプレートに渡す

    quiz = qset_data[quiz_idx]
    title = f'Quiz Web - {qset.title} [{quiz_idx + 1}]'
    return render_template(
        'quiz.html', title=title,
        qset_idx=qset_idx, qset=qset, quiz_idx=quiz_idx, quiz=quiz)


if __name__ == "__main__":
    app.run(debug=True)
