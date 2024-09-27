## 概要
**EyeDetectionApp**は、リアルタイムでカメラを使用して人の顔と目を検出し、視線情報をフィードバックする Flask アプリケーションです。このアプリは、OpenCV を使用して顔と目の位置を特定し、結果をリアルタイムで表示します。

## 主な機能
- リアルタイムでの顔検出と目の位置の追跡
- 左右の目の座標を画面に表示
- Flask を使用した Web アプリケーション
- OpenCV を利用した顔認識技術

## インストール方法

1. このリポジトリをクローンします：
    ```bash
    git clone https://github.com/CZL1998/EyeDetectionApp.git
    ```

2. 仮想環境を作成して依存パッケージをインストールします：
    ```bash
    python -m venv venv
    venv\Scripts\activate  # Windows
    pip install -r requirements.txt
    ```

3. アプリケーションを起動します：
    ```bash
    python app.py
    ```

4. ブラウザで `http://127.0.0.1:5000` にアクセスして、アプリを確認します。

## 必要条件
- Python 3.x
- Flask
- OpenCV



