@echo off
REM 仮想環境を起動
call venv\Scripts\activate

REM Flask APPを開始
python app.py

REM ブラウザで自動的に開く
start http://127.0.0.1:5000
