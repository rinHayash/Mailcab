# Mailcab
Mecabを使った言語の形態素解析ツールです。
html、テキスト、CSVに対応。

【要インストール】
・python2.7以上
・python Mecab

【使い方】
 実行ファイルと探索対象フォルダを同じ場所に置いてターミナル実行
 python mailcab.py 探索対象フォルダ 出力対象ファイル
 ex) python read.py /Users/Python/Mecab/csTest write.csv

【注意点】
対象ファイルにCSVを使う場合、文字コードUTF-8じゃないとエラーになります。
