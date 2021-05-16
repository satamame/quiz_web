# Quiz Web

## 概要

- [Flask](https://palletsprojects.com/p/flask/) を使ったクイズ出題 Web アプリです。
- クイズデータを作ってサーバに配置して、出先で単語帳のように使うことを目的としています。
- 得点をカウントしたり人と競ったりする機能はありません。

## デモ

- 動作デモは[こちら](https://honmono.no-ip.biz/quiz_web/)
    - Ubuntu 18.04.5
    - Apache 2.4.29
    - Python 3.8.0

## 使い方

- このリポジトリを Clone (またはダウンロード) して、仮想環境を作って `pip -r requirements.txt` します。
- ローカルで実行する場合はクイズデータを作って仮想環境で `python quiz_web.py` します。  
- サービスとして公開する場合は環境に合わせてデプロイしてください。

## クイズデータを作る

新規に quiz フォルダを作って、quiz_sample フォルダを参考に中身を作ります。  
quiz フォルダの中にはインデックス (1個) とクイズ集 (1個以上) を作ります。

- インデックスは index.tsv というタブ区切りテキストで、以下のフィールドを持ちます。
    1. クイズ集のファイル名
    1. クイズ集の表示名
    1. クイズ集の説明
- クイズ集は任意のファイル名のタブ区切りテキストで、以下のフィールドを持ちます。
    1. 問題文
    1. 解説文
    1. 正解文
    1. 正解以外の選択肢 (任意・複数)  
    ...

正解以外の選択肢がある場合は、選択肢が表示されます。  
正解以外の選択肢がない場合は、単に「答えを見る」というボタンが表示されます。

### Excel を使ってクイズ集を作る

quiz_sample フォルダにある .xlsm ファイルを参考に、Excel でクイズ集を作って .tsv ファイルとして保存することができます。  
この場合 .xlsm ファイルをマスターデータとして、変更を反映する際に「tsv 保存」ボタンを押して .tsv ファイルを作成/上書きします。

## デプロイ

apache2 で wsgi を使って公開する場合の例 (mod-wsgi が入っている前提) です。

1. adapter_sample.wsgi をコピーして adapter.wsgi にリネームします。
1. adapter.wsgi を編集して、3行目で insert しているパスを環境に合わせます。
1. apache2 の VirtualHost に Directory を追加し、`WSGIScriptAlias` の参照先を adapter.wsgi のパスにします。
    - 参考 : [mod-wsgi のデーモンモード](https://leadingekazuyasada.github.io/presentation/django_deploy/index.html#/daemonmode)
1. デバッグ情報をクライアント側に表示したくない場合は、`app.run(debug=True)` を `app.run()` に変更します。
1. コードを変更した場合は apache2 を再起動する必要があるようです (wsgi がキャッシュを持つのかも)。
