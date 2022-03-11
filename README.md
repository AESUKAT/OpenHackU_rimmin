# Python YouTube Tailor
<img src="pytailor.png">
youtube liveのアーカイブから、面白いと推定した区間だけを切り取って再生する

# 概要

## 背景
「推しの動画がいっぱい上がっていて、休日だけでは追いきれない…。」
「YouTube liveのアーカイブが10時間もあり、見どころがわからない…。」
そのような悩みを解消するべく製品開発を行いました。

## 製品説明
YouTube liveのアーカイブを、4つの評価基準で面白い区間を推定する。

- コメントの量
- 面白さに反応したコメント
- スーパーチャットの量
- 音量

上記の評価基準を統合して1つの面白い区間を推定する。
その後、webブラウザでその区間のみを自動で再生する。

## 今後の展望
評価アルゴリズムの改良

# 開発技術
## プログラミング言語
- python

## ライブラリ
- 標準ライブラリ
    - math
    - os
    - time
    - json

- 外部ライブラリ
    - numpy
    - librosa
    - sqlalchemy
    - selenium
    - soundfile
    - moviepy.editor
    - pytube

# 使い方
## ファイル一式のダウンロード

## 必要な外部ライブラリのインストール
```
$ pip install numpy
$ pip install librosa
$ pip install sqlalchemy
$ pip install selenium
$ pip install PySoundFile
$ pip install moviepy
$ pip install pytube
```

## 実行
ターミナルからpytailor.pyを実行した後、video idを入力する

```
$ python pytailor.py
video idを入力してください→
```
