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
    qcount = len(qset_data)

    # quiz_idx が -1 ならランダムにする
    quiz_idx = int(quiz_idx)
    if quiz_idx < 0:
        quiz_idx = random.randint(0, qcount - 1)

    # quiz_idx の位置にあるクイズを取得する
    quiz = qset_data[quiz_idx]

    # 選択肢が複数あるならランダムに並べ替える
    if len(quiz.choices) >= 2:
        choice_cnt = len(quiz.choices)
        idxs = random.sample(range(choice_cnt), choice_cnt)
        choices = [quiz.choices[i] for i in idxs]
        # 正解のインデックス
        ans_idx = idxs.index(0)
    else:
        # 選択肢が1個なら正解のインデックスを -1 にする
        choices = quiz.choices
        ans_idx = -1

    # ページを返す
    title = f'Quiz Web - {qset.title} [{quiz_idx + 1}]'
    return render_template(
        'quiz.html', title=title,
        qset_idx=qset_idx, qset=qset, qcount=qcount,
        quiz_idx=quiz_idx, quiz=quiz,
        choices=choices, ans_idx=ans_idx)


if __name__ == "__main__":
    app.run(debug=True)
