#!/bin/bash

# 仮想環境を有効化
source venv/bin/activate

# 修正したゲームを実行
python aws_cloud_master_fixed3.py

# 仮想環境を終了
deactivate
