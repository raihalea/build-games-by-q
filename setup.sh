#!/bin/bash

# 仮想環境のディレクトリ名
VENV_DIR="venv"

# 仮想環境が存在しない場合は作成
if [ ! -d "$VENV_DIR" ]; then
    echo "仮想環境を作成しています..."
    python3 -m venv $VENV_DIR
fi

# 仮想環境をアクティベート
source $VENV_DIR/bin/activate

# 必要なパッケージをインストール
echo "必要なパッケージをインストールしています..."
pip install -r requirements.txt

echo "セットアップが完了しました。"
echo "ゲームを起動するには以下のコマンドを実行してください："
echo "source venv/bin/activate && python aws_cloud_master.py"
