#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import sys
import random
import os
import math
from pygame.locals import *
from player_actions import player_actions, execute_player_action
from player_actions import player_actions, execute_player_action

# 初期化
pygame.init()

# 画面サイズ
SCREEN_WIDTH = 1280  # 画面幅を広げる
SCREEN_HEIGHT = 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('AWS Cloud Master')

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)
ORANGE = (255, 165, 0)
AWS_ORANGE = (255, 153, 0)
AWS_BLUE = (51, 153, 255)
AWS_GREEN = (35, 134, 54)
CHART_COLORS = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0)]  # チャート用の色

# イベントタイプの色
EVENT_EXTERNAL = AWS_ORANGE  # 外部要因イベントの色
EVENT_INTERNAL = LIGHT_BLUE  # 内部要因イベントの色

# フォントの設定
font_path = os.path.join('assets', 'fonts', 'extracted', 'static', 'NotoSansJP-Regular.ttf')
title_font = pygame.font.Font(font_path, 48)
normal_font = pygame.font.Font(font_path, 24)
small_font = pygame.font.Font(font_path, 18)

# AWSサービスのカード情報
aws_services = [
    {"name": "Amazon EC2", "description": "仮想サーバーを提供するサービス", "cost": 5, "revenue": 3, "category": "コンピューティング"},
    {"name": "Amazon S3", "description": "スケーラブルなオブジェクトストレージ", "cost": 3, "revenue": 2, "category": "ストレージ"},
    {"name": "Amazon RDS", "description": "リレーショナルデータベースサービス", "cost": 6, "revenue": 4, "category": "データベース"},
    {"name": "Amazon DynamoDB", "description": "NoSQLデータベースサービス", "cost": 4, "revenue": 3, "category": "データベース"},
    {"name": "AWS Lambda", "description": "サーバーレスコンピューティング", "cost": 2, "revenue": 3, "category": "コンピューティング"},
    {"name": "Amazon VPC", "description": "仮想プライベートクラウド", "cost": 3, "revenue": 2, "category": "ネットワーキング"},
    {"name": "Amazon CloudFront", "description": "コンテンツ配信ネットワーク", "cost": 4, "revenue": 3, "category": "ネットワーキング"},
    {"name": "AWS IAM", "description": "アイデンティティとアクセス管理", "cost": 1, "revenue": 2, "category": "セキュリティ"},
    {"name": "Amazon SNS", "description": "通知サービス", "cost": 2, "revenue": 1, "category": "アプリケーション統合"},
    {"name": "Amazon SQS", "description": "メッセージキューイングサービス", "cost": 2, "revenue": 1, "category": "アプリケーション統合"},
    {"name": "AWS CloudFormation", "description": "インフラストラクチャのコード化", "cost": 1, "revenue": 3, "category": "管理ツール"},
    {"name": "Amazon CloudWatch", "description": "モニタリングサービス", "cost": 2, "revenue": 2, "category": "管理ツール"},
    {"name": "AWS Auto Scaling", "description": "自動スケーリングサービス", "cost": 3, "revenue": 4, "category": "管理ツール"},
    {"name": "Amazon ECS", "description": "コンテナオーケストレーション", "cost": 4, "revenue": 5, "category": "コンピューティング"},
    {"name": "AWS Fargate", "description": "サーバーレスコンテナ", "cost": 3, "revenue": 4, "category": "コンピューティング"},
    {"name": "Amazon EKS", "description": "マネージドKubernetes", "cost": 5, "revenue": 6, "category": "コンピューティング"},
    {"name": "Amazon ElastiCache", "description": "インメモリキャッシュ", "cost": 4, "revenue": 3, "category": "データベース"},
    {"name": "Amazon Redshift", "description": "データウェアハウス", "cost": 7, "revenue": 8, "category": "データベース"},
    {"name": "AWS Step Functions", "description": "ワークフロー管理", "cost": 3, "revenue": 2, "category": "アプリケーション統合"},
    {"name": "Amazon API Gateway", "description": "APIの作成と管理", "cost": 3, "revenue": 3, "category": "ネットワーキング"},
]

# 外部要因イベント情報
external_events = [
    {"name": "自社サービスのブーム", "description": "SNSで話題になり新規ユーザーが増加", "effect": "顧客+5", "duration": 3, "type": "boom"},
    {"name": "競合他社の台頭", "description": "競合他社に顧客を奪われる", "effect": "顧客-3", "duration": 2, "type": "competition"},
    {"name": "セキュリティインシデント", "description": "データ漏洩の可能性が報道される", "effect": "顧客-5", "duration": 3, "type": "security_issue"},
    {"name": "市場の拡大", "description": "業界全体の需要が増加", "effect": "顧客+3", "duration": 4, "type": "market_growth"},
    {"name": "経済不況", "description": "景気後退により顧客の予算が削減", "effect": "クレジット-2", "duration": 3, "type": "recession"},
    {"name": "技術トレンドの変化", "description": "新技術への移行が求められる", "effect": "クレジット-3", "duration": 2, "type": "tech_trend"},
    {"name": "業界規制の強化", "description": "コンプライアンス対応が必要", "effect": "クレジット-2", "duration": 4, "type": "regulation"},
    {"name": "クラウド利用の普及", "description": "クラウドサービスの需要増加", "effect": "顧客+4", "duration": 3, "type": "cloud_adoption"},
]

# 内部要因イベント情報
internal_events = [
    {"name": "サーバーレス移行", "description": "EC2からLambdaへの移行でコスト削減", "effect": "クレジット+3", "counter_effect": {"boom": 2, "cloud_adoption": 1}},
    {"name": "セキュリティ監査", "description": "IAMポリシーの見直しが必要", "effect": "次のターンスキップ", "counter_effect": {"security_issue": -2}},
    {"name": "クラウド最適化", "description": "リソース最適化でコスト削減", "effect": "クレジット+2", "counter_effect": {"recession": -1}},
    {"name": "新規プロジェクト", "description": "新しいサービスの追加が必要", "effect": "追加サービス+1", "counter_effect": {"market_growth": 1}},
    {"name": "バックアップ強化", "description": "データ復旧体制の強化", "effect": "クレジット-1", "counter_effect": {"security_issue": -1}},
    {"name": "AWS認定取得", "description": "チームのスキル向上", "effect": "クレジット+2", "counter_effect": {"tech_trend": -1}},
    {"name": "マーケティング強化", "description": "広告宣伝の強化", "effect": "クレジット-2", "counter_effect": {"boom": 1, "competition": -1}},
    {"name": "コスト最適化", "description": "リザーブドインスタンスの購入", "effect": "クレジット+4", "counter_effect": {"recession": -2}},
    {"name": "コンプライアンス対応", "description": "規制対応のための体制整備", "effect": "クレジット-2", "counter_effect": {"regulation": -2}},
    {"name": "クラウドマイグレーション", "description": "オンプレミスからAWSへの移行", "effect": "クレジット+3", "counter_effect": {"cloud_adoption": 2}},
]

# イベントデッキの作成（外部要因と内部要因を合わせる）
events = external_events + internal_events

# イベント名と説明のテンプレート
event_names = {
    "market": ["市場の", "業界の", "顧客の", "需要の", "ビジネスの"],
    "tech": ["技術の", "システムの", "インフラの", "クラウドの", "アーキテクチャの"],
    "security": ["セキュリティの", "保護の", "防御の", "安全性の", "リスクの"],
    "cost": ["コストの", "予算の", "支出の", "投資の", "財務の"]
}

event_changes = {
    "positive": ["拡大", "向上", "改善", "成長", "進化", "最適化"],
    "negative": ["縮小", "悪化", "低下", "減少", "問題", "課題"]
}

event_descriptions = {
    "market": {
        "positive": ["新規顧客の獲得に成功", "市場シェアが拡大", "ユーザー数が増加", "ビジネスチャンスが増加"],
        "negative": ["顧客離れが発生", "市場シェアが縮小", "競合他社に顧客を奪われる", "需要が減少"]
    },
    "tech": {
        "positive": ["新技術の導入に成功", "システム効率が向上", "パフォーマンスが改善", "スケーラビリティが向上"],
        "negative": ["技術的負債の増加", "システム障害の発生", "パフォーマンス低下", "互換性の問題"]
    },
    "security": {
        "positive": ["セキュリティ体制の強化", "脆弱性の修正完了", "防御システムの改善", "監視体制の強化"],
        "negative": ["セキュリティホールの発見", "脆弱性の露呈", "不正アクセスの試み", "データ保護の課題"]
    },
    "cost": {
        "positive": ["コスト削減の成功", "予算の最適化", "投資効率の向上", "ROIの改善"],
        "negative": ["予期せぬコスト増加", "予算超過", "投資効果の低下", "維持費の増大"]
    }
}

# 動的にイベントを生成する関数
def generate_random_event():
    # イベントの種類をランダムに選択
    event_category = random.choice(["market", "tech", "security", "cost"])
    # ポジティブかネガティブかをランダムに決定
    sentiment = random.choice(["positive", "negative"])
    
    # イベント名の生成
    name_prefix = random.choice(event_names[event_category])
    name_suffix = random.choice(event_changes[sentiment])
    event_name = f"{name_prefix}{name_suffix}"
    
    # イベント説明の生成
    event_description = random.choice(event_descriptions[event_category][sentiment])
    
    # 効果の生成
    effect_type = ""
    if event_category in ["market"]:
        effect_type = "顧客"
    else:
        effect_type = "クレジット"
    
    # 効果の値を決定
    if sentiment == "positive":
        effect_value = random.randint(2, 5)
        effect = f"{effect_type}+{effect_value}"
    else:
        effect_value = random.randint(1, 4)
        effect = f"{effect_type}-{effect_value}"
    
    # 持続期間を決定
    duration = random.randint(2, 4)
    
    # イベントタイプを決定
    event_type = f"{event_category}_{sentiment}"
    
    # 対抗効果を生成（50%の確率で）
    counter_effect = None
    if random.random() < 0.5:
        counter_effect = {}
        # 1〜2個の対抗効果を追加
        counter_types = ["boom", "competition", "security_issue", "market_growth", 
                        "recession", "tech_trend", "regulation", "cloud_adoption"]
        num_counters = random.randint(1, 2)
        for _ in range(num_counters):
            counter_type = random.choice(counter_types)
            # -2から+2の範囲で効果を設定
            modifier = random.randint(-2, 2)
            if modifier != 0:  # 0の場合は効果なしなので追加しない
                counter_effect[counter_type] = modifier
    
    # イベントオブジェクトを作成
    event = {
        "name": event_name,
        "description": event_description,
        "effect": effect,
        "duration": duration,
        "type": event_type
    }
    
    # 対抗効果がある場合は追加
    if counter_effect and len(counter_effect) > 0:
        event["counter_effect"] = counter_effect
    
    return event
# プレイヤークラス
class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.position = 0
        self.credits = 20  # 初期クレジット
        self.services = []  # 獲得したAWSサービス
        self.skip_turn = False
        self.revenue_per_turn = 2  # 毎ターンの基本収入
        self.credit_history = [20]  # クレジット履歴（チャート表示用）
        self.customers = 10  # 初期顧客数
        self.customer_history = [10]  # 顧客数履歴
        self.active_external_events = []  # アクティブな外部要因イベント
        self.active_internal_events = []  # アクティブな内部要因イベント

    def calculate_revenue(self):
        # 基本収入 + サービスからの収入 + 顧客数に応じた収入
        total_revenue = self.revenue_per_turn
        
        # サービスからの収入
        for service in self.services:
            total_revenue += service["revenue"]
        
        # 顧客数に応じた追加収入（顧客10人ごとに1クレジット）
        customer_bonus = self.customers // 10
        total_revenue += customer_bonus
        
        return total_revenue
        
    def update_credit_history(self):
        # 現在のクレジットを履歴に追加
        self.credit_history.append(self.credits)
        
    def update_customer_history(self):
        # 現在の顧客数を履歴に追加
        self.customer_history.append(self.customers)
        
    def apply_active_events(self):
        # アクティブな外部要因イベントの効果を適用
        for event in self.active_external_events[:]:  # リストのコピーを使用して反復中に削除できるようにする
            # イベントの効果を適用
            effect = event["effect"]
            if "クレジット" in effect:
                value = int(effect.split("+")[1] if "+" in effect else effect.split("-")[1])
                if "+" in effect:
                    self.credits += value
                else:
                    self.credits -= value
                    if self.credits < 0:
                        self.credits = 0
            
            elif "顧客" in effect:
                value = int(effect.split("+")[1] if "+" in effect else effect.split("-")[1])
                if "+" in effect:
                    self.customers += value
                else:
                    self.customers -= value
                    if self.customers < 0:
                        self.customers = 0
            
            # イベントの残りターン数を減らす
            event["remaining_turns"] -= 1
            
            # ターン数が0になったらイベントを削除
            if event["remaining_turns"] <= 0:
                self.active_external_events.remove(event)
        
        # アクティブな内部要因イベントの残りターン数を減らす
        for event in self.active_internal_events[:]:
            event["remaining_turns"] -= 1
            if event["remaining_turns"] <= 0:
                self.active_internal_events.remove(event)
        
        # 履歴を更新
        self.update_credit_history()
        self.update_customer_history()
        
    def add_external_event(self, event):
        # 外部要因イベントを追加
        # イベントのコピーを作成して残りターン数を設定
        event_copy = event.copy()
        event_copy["remaining_turns"] = event["duration"]
        
        # 同じタイプのイベントがすでにある場合は置き換える
        for i, active_event in enumerate(self.active_external_events):
            if active_event["type"] == event["type"]:
                self.active_external_events[i] = event_copy
                return
        
        # 新しいイベントを追加
        self.active_external_events.append(event_copy)
        
    def apply_internal_event(self, event):
        # 内部要因イベントの効果を適用
        effect = event["effect"]
        
        # 基本効果の適用
        if "クレジット" in effect:
            value = int(effect.split("+")[1] if "+" in effect else effect.split("-")[1])
            if "+" in effect:
                self.credits += value
            else:
                self.credits -= value
                if self.credits < 0:
                    self.credits = 0
            self.update_credit_history()
        
        elif "顧客" in effect:
            value = int(effect.split("+")[1] if "+" in effect else effect.split("-")[1])
            if "+" in effect:
                self.customers += value
            else:
                self.customers -= value
                if self.customers < 0:
                    self.customers = 0
            self.update_customer_history()
        
        elif "次のターンスキップ" in effect:
            self.skip_turn = True
        
        elif "追加サービス" in effect:
            if service_deck:
                extra_service = service_deck.pop()
                if self.credits >= extra_service["cost"]:
                    self.services.append(extra_service)
                    self.credits -= extra_service["cost"]
        
        # 対抗効果を持つ内部要因イベントはアクティブイベントリストに追加
        if "counter_effect" in event:
            # イベントの持続期間を設定（内部要因イベントは基本的に3ターン）
            event_copy = event.copy()
            event_copy["remaining_turns"] = 3  # 内部要因イベントの標準持続期間
            self.active_internal_events.append(event_copy)
            
            # 外部要因イベントへの対抗効果を適用
            for event_type, modifier in event["counter_effect"].items():
                for active_event in self.active_external_events:
                    if active_event["type"] == event_type:
                        # 対抗効果の適用（効果の強化または弱体化）
                        if modifier > 0:  # 強化
                            effect = active_event["effect"]
                            if "クレジット+" in effect:
                                value = int(effect.split("+")[1]) + modifier
                                active_event["effect"] = f"クレジット+{value}"
                            elif "顧客+" in effect:
                                value = int(effect.split("+")[1]) + modifier
                                active_event["effect"] = f"顧客+{value}"
                        elif modifier < 0:  # 弱体化（絶対値を減らす）
                            effect = active_event["effect"]
                            if "クレジット-" in effect:
                                value = max(0, int(effect.split("-")[1]) + modifier)  # 0未満にならないように
                                active_event["effect"] = f"クレジット-{value}"
                            elif "顧客-" in effect:
                                value = max(0, int(effect.split("-")[1]) + modifier)  # 0未満にならないように
                                active_event["effect"] = f"顧客-{value}"
# レイアウト設定
info_panel_x = SCREEN_WIDTH // 2 + 20  # 情報パネルのX座標（右半分の開始位置）
info_panel_width = SCREEN_WIDTH - info_panel_x - 20  # 情報パネルの幅
chart_height = 200  # チャートの高さ

# ゲームボードの設定
board_positions = 24
board_size = min(SCREEN_WIDTH // 2, SCREEN_HEIGHT - chart_height - 120) - 20  # ボードサイズを調整（バナー分も考慮）
board_center_x = SCREEN_WIDTH // 4  # ボードを左側に配置
board_center_y = chart_height + 120 + board_size // 2  # バナーの下に配置
board_radius = board_size // 2

# プレイヤーの初期化
players = [
    Player("プレイヤー1", (255, 0, 0)),
    Player("プレイヤー2", (0, 0, 255)),
]
current_player_index = 0

# カードデッキの初期化
service_deck = aws_services.copy()
random.shuffle(service_deck)

# 現在のカードとイベント
current_service = None
current_event = None

# ゲームの状態
game_state = "ROLL"  # "ROLL", "SERVICE", "EVENT", "ACTION", "TARGET", "ACTION_RESULT", "END"
winner = None
dice_value = 0

# アクション関連のグローバル変数
action_buttons = []
cancel_button = None
target_buttons = []
ok_button = None
result_message = ""
current_action = None
turn_count = 1
max_turns = 20  # 最大ターン数
current_action = None  # 選択中のプレイヤーアクション
# ボタンクラス
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.enabled = True  # ボタンの有効/無効状態

    def draw(self):
        # 有効/無効状態に応じて色を決定
        if self.enabled:
            color = self.hover_color if self.is_hovered else self.color
            text_color = BLACK
            border_color = BLACK
        else:
            # 無効時はグレースケール化
            color = (150, 150, 150)  # 濃いグレー（通常時）
            text_color = (80, 80, 80)  # 暗いグレー
            border_color = (100, 100, 100)  # 中間のグレー
        
        # ボタンの背景
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        
        # ボタンの枠線
        pygame.draw.rect(screen, border_color, self.rect, 2, border_radius=5)
        
        # 無効時は斜線を追加して視覚的に無効であることを強調
        if not self.enabled:
            # 左上から右下への斜線
            pygame.draw.line(screen, (100, 100, 100), 
                            (self.rect.left + 5, self.rect.top + 5), 
                            (self.rect.right - 5, self.rect.bottom - 5), 2)
            # 右上から左下への斜線
            pygame.draw.line(screen, (100, 100, 100), 
                            (self.rect.right - 5, self.rect.top + 5), 
                            (self.rect.left + 5, self.rect.bottom - 5), 2)
        
        # テキスト
        text_surface = normal_font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos) and self.enabled
        return self.is_hovered

    def is_clicked(self, pos, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1 and self.enabled:
            return self.rect.collidepoint(pos)
        return False
# ボタンの作成と配置
button_width = 100  # ボタン幅を小さくする
button_height = 40  # ボタン高さも少し小さくする
button_margin = 8   # 余白も少し小さくする

# 右側パネルの下部に横一列に配置
info_panel_x = SCREEN_WIDTH // 2 + 20  # 情報パネルのX座標（右半分の開始位置）
info_panel_width = SCREEN_WIDTH - info_panel_x - 20  # 情報パネルの幅

# 4つのボタンを横一列に配置するための計算
total_buttons_width = (button_width * 4) + (button_margin * 3)  # 4つのボタン + 3つの余白
start_x = info_panel_x + (info_panel_width - total_buttons_width) // 2  # 中央揃え

# ボタンを横一列に配置
roll_button = Button(start_x, SCREEN_HEIGHT - button_height - button_margin, 
                    button_width, button_height, "サイコロ", LIGHT_BLUE, (100, 200, 255))

buy_button = Button(start_x + button_width + button_margin, SCREEN_HEIGHT - button_height - button_margin, 
                   button_width, button_height, "導入", AWS_ORANGE, (255, 200, 100))

skip_button = Button(start_x + (button_width + button_margin) * 2, SCREEN_HEIGHT - button_height - button_margin, 
                    button_width, button_height, "スキップ", GRAY, (150, 150, 150))

# アクションボタンを追加
action_button = Button(start_x + (button_width + button_margin) * 3, SCREEN_HEIGHT - button_height - button_margin, 
                      button_width, button_height, "アクション", AWS_GREEN, (100, 255, 150))

# レイアウト設定
chart_height = 200  # チャートの高さ
# サイコロを振る関数
def roll_dice():
    return random.randint(1, 6)

# ボードの描画
def draw_board():
    # ボードの背景
    pygame.draw.circle(screen, LIGHT_BLUE, (board_center_x, board_center_y), board_radius)
    pygame.draw.circle(screen, WHITE, (board_center_x, board_center_y), board_radius - 50)
    
    # マスの描画
    for i in range(board_positions):
        angle = 2 * math.pi * i / board_positions
        x = board_center_x + int((board_radius - 25) * math.cos(angle))
        y = board_center_y + int((board_radius - 25) * math.sin(angle))
        
        # マスの種類によって色を変える
        if i % 3 == 0:
            color = AWS_ORANGE  # サービスマス
        elif i % 3 == 1:
            color = AWS_BLUE  # イベントマス
        else:
            color = GRAY  # 通常マス
            
        pygame.draw.circle(screen, color, (x, y), 20)
        pygame.draw.circle(screen, BLACK, (x, y), 20, 2)
        
        # マス番号
        text = small_font.render(str(i+1), True, BLACK)
        text_rect = text.get_rect(center=(x, y))
        screen.blit(text, text_rect)

# プレイヤーの描画
def draw_players():
    for i, player in enumerate(players):
        angle = 2 * math.pi * player.position / board_positions
        offset = 10 * (i - len(players) / 2 + 0.5)  # プレイヤーが重ならないようにオフセット
        x = board_center_x + int((board_radius - 25) * math.cos(angle)) + offset
        y = board_center_y + int((board_radius - 25) * math.sin(angle))
        
        pygame.draw.circle(screen, player.color, (x, y), 15)
        pygame.draw.circle(screen, BLACK, (x, y), 15, 2)

# プレイヤー情報の描画
def draw_player_info():
    info_panel_y = banner_bottom + 10  # バナーの下に配置
    
    # プレイヤー数に応じてパネルの高さを調整（横並びなので高さは固定）
    panel_height = 140  # 高さをさらに増やす
    
    # 情報パネルの背景
    pygame.draw.rect(screen, LIGHT_BLUE, (info_panel_x, info_panel_y, info_panel_width, panel_height), border_radius=5)
    pygame.draw.rect(screen, BLACK, (info_panel_x, info_panel_y, info_panel_width, panel_height), 2, border_radius=5)
    
    # パネルタイトル
    title_text = normal_font.render("プレイヤー情報", True, BLACK)
    screen.blit(title_text, (info_panel_x + 10, info_panel_y + 10))
    
    # 各プレイヤーを横に並べる
    player_width = info_panel_width // len(players) - 10  # 各プレイヤーの幅（余白を考慮）
    
    for i, player in enumerate(players):
        x_offset = i * (player_width + 10) + 10  # 各プレイヤーの横位置（10pxの余白）
        
        # プレイヤー名と背景 - 高さを増やす
        pygame.draw.rect(screen, player.color, (info_panel_x + x_offset, info_panel_y + 40, player_width, 90), border_radius=5)
        pygame.draw.rect(screen, BLACK, (info_panel_x + x_offset, info_panel_y + 40, player_width, 90), 2, border_radius=5)
        
        # プレイヤー情報テキスト
        name_text = normal_font.render(player.name, True, BLACK)
        name_rect = name_text.get_rect(center=(info_panel_x + x_offset + player_width // 2, info_panel_y + 55))
        screen.blit(name_text, name_rect)
        
        # クレジットと収入を短縮表示
        credits_text = small_font.render(f"¥{player.credits}", True, BLACK)
        credits_rect = credits_text.get_rect(center=(info_panel_x + x_offset + player_width // 2, info_panel_y + 75))
        screen.blit(credits_text, credits_rect)
        
        # 収入を表示
        revenue_text = small_font.render(f"+¥{player.calculate_revenue()}/ターン", True, BLACK)
        revenue_rect = revenue_text.get_rect(center=(info_panel_x + x_offset + player_width // 2, info_panel_y + 95))
        screen.blit(revenue_text, revenue_rect)
        
        # 顧客数を表示
        customer_text = small_font.render(f"顧客: {player.customers}人", True, BLACK)
        customer_rect = customer_text.get_rect(center=(info_panel_x + x_offset + player_width // 2, info_panel_y + 115))
        screen.blit(customer_text, customer_rect)
        
        # 現在のプレイヤーを示す
        if i == current_player_index:
            pygame.draw.rect(screen, WHITE, (info_panel_x + x_offset - 2, info_panel_y + 38, player_width + 4, 94), 3, border_radius=8)
    
    return info_panel_y + panel_height  # 次の要素の開始Y座標を返す

# ゲーム情報の描画
def draw_game_info():
    # 情報パネルの背景 - 右側に配置
    pygame.draw.rect(screen, AWS_BLUE, (info_panel_x, banner_bottom + 10, info_panel_width, 60), border_radius=5)
    pygame.draw.rect(screen, BLACK, (info_panel_x, banner_bottom + 10, info_panel_width, 60), 2, border_radius=5)
    
    # ゲームの状態
    state_text = ""
    if game_state == "ROLL":
        state_text = "サイコロを振ってください"
    elif game_state == "SERVICE":
        state_text = "サービス導入の判断"
    elif game_state == "EVENT":
        state_text = "イベント発生"
    elif game_state == "ACTION":
        state_text = "プレイヤーアクション選択"
    elif game_state == "TARGET":
        state_text = "アクション対象選択"
    elif game_state == "ACTION_RESULT":
        state_text = "アクション結果"
    elif game_state == "END":
        state_text = "ゲーム終了"
        
    # ゲーム状態を表示
    state_text_render = normal_font.render(f"状態: {state_text}", True, WHITE)
    screen.blit(state_text_render, (info_panel_x + 10, banner_bottom + 25))
# サイコロの描画
def draw_dice():
    # サイコロの結果をボタンの左に表示
    if dice_value > 0:
        # ボタンの左側にサイコロを表示
        dice_size = 40  # サイコロのサイズをさらに小さく
        dice_margin = 10  # サイコロとボタンの間の余白
        
        # サイコロを振るボタンの左側に配置
        dice_x = roll_button.rect.x - dice_size - dice_margin
        dice_y = roll_button.rect.y + (roll_button.rect.height - dice_size) // 2  # ボタンと垂直方向に中央揃え
        
        # サイコロの背景
        dice_bg = pygame.Rect(dice_x, dice_y, dice_size, dice_size)
        pygame.draw.rect(screen, LIGHT_BLUE, dice_bg, border_radius=8)
        pygame.draw.rect(screen, BLACK, dice_bg, 2, border_radius=8)
        
        # サイコロの目
        dice_text = normal_font.render(str(dice_value), True, BLACK)  # フォントサイズを小さく
        dice_rect = dice_text.get_rect(center=dice_bg.center)
        screen.blit(dice_text, dice_rect)
        
        # サイコロのラベル
        dice_label = small_font.render("出目", True, BLACK)
        dice_label_rect = dice_label.get_rect(center=(dice_x + dice_size // 2, dice_y - 10))
        screen.blit(dice_label, dice_label_rect)

# カード情報の描画
def draw_card_info():
    # カードを左側のボード中心にポップアップ表示
    if current_service or current_event:
        # カードサイズと位置の設定
        card_width = 300
        card_height = 200
        card_x = board_center_x - card_width // 2  # ボードの中心に配置
        card_y = board_center_y - card_height // 2  # ボードの中心に配置
        
        # バナーの下端を取得（オーバーレイの開始位置として使用）
        overlay_start_y = banner_bottom  # バナーの下端からオーバーレイを開始
        
        # 半透明の背景オーバーレイ（左側のボード部分のみ - バナーの下から開始）
        overlay = pygame.Surface((SCREEN_WIDTH // 2, SCREEN_HEIGHT - overlay_start_y))
        overlay.set_alpha(150)  # 透明度の設定
        overlay.fill(BLACK)
        # バナーの下から開始
        screen.blit(overlay, (0, overlay_start_y))
        
        if current_service:
            # サービスカードの背景
            pygame.draw.rect(screen, LIGHT_BLUE, (card_x, card_y, card_width, card_height), border_radius=10)
            pygame.draw.rect(screen, BLACK, (card_x, card_y, card_width, card_height), 2, border_radius=10)
            
            # サービス情報
            name_text = normal_font.render(current_service["name"], True, BLACK)
            name_rect = name_text.get_rect(center=(card_x + card_width // 2, card_y + 25))
            screen.blit(name_text, name_rect)
            
            desc_text = small_font.render(current_service["description"], True, BLACK)
            desc_rect = desc_text.get_rect(center=(card_x + card_width // 2, card_y + 55))
            screen.blit(desc_text, desc_rect)
            
            category_text = small_font.render(f"カテゴリ: {current_service['category']}", True, BLACK)
            screen.blit(category_text, (card_x + 20, card_y + 85))
            
            cost_text = small_font.render(f"導入コスト: {current_service['cost']}", True, BLACK)
            screen.blit(cost_text, (card_x + 20, card_y + 115))
            
            revenue_text = small_font.render(f"収入/ターン: +{current_service['revenue']}", True, AWS_GREEN)
            screen.blit(revenue_text, (card_x + 20, card_y + 145))
            
            # 導入可能かどうかを表示
            current_player = players[current_player_index]
            if current_player.credits >= current_service["cost"]:
                status_text = small_font.render("導入可能", True, AWS_GREEN)
            else:
                status_text = small_font.render("クレジット不足", True, (255, 0, 0))
            status_rect = status_text.get_rect(center=(card_x + card_width // 2, card_y + 175))
            screen.blit(status_text, status_rect)
            
        elif current_event:
            # イベントカードの背景 - 高さを拡大して情報を追加表示
            card_height = 250  # 高さを拡大
            card_y = board_center_y - card_height // 2  # 位置を再調整
            
            pygame.draw.rect(screen, AWS_ORANGE, (card_x, card_y, card_width, card_height), border_radius=10)
            pygame.draw.rect(screen, BLACK, (card_x, card_y, card_width, card_height), 2, border_radius=10)
            
            # イベント情報
            name_text = normal_font.render(current_event["name"], True, BLACK)
            name_rect = name_text.get_rect(center=(card_x + card_width // 2, card_y + 25))
            screen.blit(name_text, name_rect)
            
            desc_text = small_font.render(current_event["description"], True, BLACK)
            desc_rect = desc_text.get_rect(center=(card_x + card_width // 2, card_y + 55))
            screen.blit(desc_text, desc_rect)
            
            # 効果の表示（顧客数の変動も含む）
            effect = current_event["effect"]
            effect_color = BLACK
            
            if "クレジット+" in effect or "顧客+" in effect:
                effect_color = AWS_GREEN
            elif "クレジット-" in effect or "顧客-" in effect:
                effect_color = (255, 0, 0)
                
            effect_text = small_font.render(f"効果: {effect}", True, effect_color)
            effect_rect = effect_text.get_rect(center=(card_x + card_width // 2, card_y + 85))
            screen.blit(effect_text, effect_rect)
            
            # 持続期間の表示（外部要因イベントの場合）
            if "duration" in current_event:
                duration_text = small_font.render(f"持続期間: {current_event['duration']}ターン", True, BLACK)
                duration_rect = duration_text.get_rect(center=(card_x + card_width // 2, card_y + 115))
                screen.blit(duration_text, duration_rect)
            
            # 対抗効果の表示（内部要因イベントの場合）
            if "counter_effect" in current_event:
                counter_text = small_font.render("対抗効果:", True, BLACK)
                screen.blit(counter_text, (card_x + 20, card_y + 145))
                
                # 対抗効果の詳細を表示
                y_offset = 0
                for event_type, modifier in current_event["counter_effect"].items():
                    # 対抗効果の説明テキスト
                    effect_desc = ""
                    if modifier > 0:
                        effect_desc = f"{event_type}に対して強化 (+{modifier})"
                        effect_color = AWS_GREEN
                    else:
                        effect_desc = f"{event_type}に対して軽減 ({modifier})"
                        effect_color = (255, 0, 0)
                    
                    counter_detail = small_font.render(effect_desc, True, effect_color)
                    screen.blit(counter_detail, (card_x + 30, card_y + 165 + y_offset))
                    y_offset += 20
                    
                    # 最大2つまで表示（スペースの制約）
                    if y_offset >= 40:
                        more_text = small_font.render("...", True, BLACK)
                        screen.blit(more_text, (card_x + 30, card_y + 165 + y_offset))
                        break
# ゲームの勝者を決定する
def check_winner():
    if turn_count > max_turns:  # 最大ターン数でゲーム終了
        max_credits = -1
        winner = None
        
        for player in players:
            if player.credits > max_credits:
                max_credits = player.credits
                winner = player
        
        return winner
    return None

# イベントの効果を適用
def apply_event_effect(player, event):
    effect = event["effect"]
    
    if "クレジット" in effect:
        value = int(effect.split("+")[1] if "+" in effect else effect.split("-")[1])
        if "+" in effect:
            player.credits += value
            player.update_credit_history()  # クレジット履歴を更新
        else:
            player.credits -= value
            if player.credits < 0:
                player.credits = 0
            player.update_credit_history()  # クレジット履歴を更新
    
    elif "顧客" in effect:
        value = int(effect.split("+")[1] if "+" in effect else effect.split("-")[1])
        if "+" in effect:
            player.customers += value
        else:
            player.customers -= value
            if player.customers < 0:
                player.customers = 0
        player.update_customer_history()  # 顧客数履歴を更新
    
    elif "次のターンスキップ" in effect:
        player.skip_turn = True
    
    elif "追加サービス" in effect:
        if service_deck:
            extra_service = service_deck.pop()
            if player.credits >= extra_service["cost"]:
                player.services.append(extra_service)
                player.credits -= extra_service["cost"]
    
    # 外部要因イベントの場合、アクティブイベントリストに追加
    if "duration" in event:
        event_copy = event.copy()
        event_copy["remaining_turns"] = event["duration"]
        player.active_external_events.append(event_copy)
    # 内部要因イベントの場合、対抗効果があればアクティブイベントリストに追加
    elif "counter_effect" in event:
        player.apply_internal_event(event)

# 毎ターンの収入を適用
def apply_turn_revenue(player):
    revenue = player.calculate_revenue()
    player.credits += revenue
    player.update_credit_history()  # クレジット履歴を更新
    
    # 顧客数の自然増加（サービス数に応じて増加）
    if player.services:
        natural_growth = len(player.services) // 2  # サービス2つごとに1人の顧客増加
        if natural_growth > 0:
            player.customers += natural_growth
            player.update_customer_history()
    
    return revenue

# サービスとイベント情報の描画
def draw_services_and_events(player):
    # プレイヤー情報パネルの下に配置するため、Y座標を計算
    panel_x = info_panel_x
    panel_y = next_panel_y + 10  # プレイヤー情報パネルの下に10pxの余白を空けて配置
    panel_width = info_panel_width
    panel_height = 250  # 高さを拡大して情報を追加表示
    
    pygame.draw.rect(screen, LIGHT_BLUE, (panel_x, panel_y, panel_width, panel_height), border_radius=5)
    pygame.draw.rect(screen, BLACK, (panel_x, panel_y, panel_width, panel_height), 2, border_radius=5)
    
    # タブ表示のようなデザイン
    tab_width = panel_width // 2 - 10
    
    # サービスタブ
    pygame.draw.rect(screen, AWS_BLUE, (panel_x + 5, panel_y + 5, tab_width, 30), border_radius=5)
    pygame.draw.rect(screen, BLACK, (panel_x + 5, panel_y + 5, tab_width, 30), 2, border_radius=5)
    service_tab_text = normal_font.render("導入済みサービス", True, WHITE)
    service_tab_rect = service_tab_text.get_rect(center=(panel_x + 5 + tab_width // 2, panel_y + 20))
    screen.blit(service_tab_text, service_tab_rect)
    
    # イベントタブ
    pygame.draw.rect(screen, AWS_ORANGE, (panel_x + panel_width - tab_width - 5, panel_y + 5, tab_width, 30), border_radius=5)
    pygame.draw.rect(screen, BLACK, (panel_x + panel_width - tab_width - 5, panel_y + 5, tab_width, 30), 2, border_radius=5)
    event_tab_text = normal_font.render("アクティブイベント", True, WHITE)
    event_tab_rect = event_tab_text.get_rect(center=(panel_x + panel_width - tab_width - 5 + tab_width // 2, panel_y + 20))
    screen.blit(event_tab_text, event_tab_rect)
    
    # コンテンツ領域
    content_y = panel_y + 40
    content_height = panel_height - 45
    
    # 左側: サービス一覧
    service_x = panel_x + 10
    service_width = panel_width // 2 - 15
    
    pygame.draw.rect(screen, WHITE, (service_x, content_y, service_width, content_height), border_radius=5)
    pygame.draw.rect(screen, BLACK, (service_x, content_y, service_width, content_height), 1, border_radius=5)
    
    # サービスがない場合のメッセージ
    if len(player.services) == 0:
        no_service_text = small_font.render("導入済みのサービスはありません", True, BLACK)
        text_rect = no_service_text.get_rect(center=(service_x + service_width // 2, content_y + content_height // 2))
        screen.blit(no_service_text, text_rect)
    else:
        # スクロール可能なサービス一覧
        max_visible_services = 8  # 一度に表示する最大サービス数
        
        # サービス一覧
        for i, service in enumerate(player.services):
            if i >= max_visible_services:  # 最大表示数を超えた場合
                more_text = small_font.render(f"...他 {len(player.services) - max_visible_services} サービス", True, BLACK)
                screen.blit(more_text, (service_x + 5, content_y + 5 + max_visible_services * 20))
                break
                
            service_text = small_font.render(f"{service['name']} (+{service['revenue']})", True, BLACK)
            screen.blit(service_text, (service_x + 5, content_y + 5 + i * 20))  # 行間を狭くする
    
    # 右側: アクティブイベント一覧
    event_x = panel_x + panel_width // 2 + 5
    event_width = panel_width // 2 - 15
    
    pygame.draw.rect(screen, WHITE, (event_x, content_y, event_width, content_height), border_radius=5)
    pygame.draw.rect(screen, BLACK, (event_x, content_y, event_width, content_height), 1, border_radius=5)
    
    # すべてのアクティブイベントを結合
    all_active_events = player.active_external_events + player.active_internal_events
    
    # アクティブイベントがない場合のメッセージ
    if len(all_active_events) == 0:
        no_event_text = small_font.render("アクティブなイベントはありません", True, BLACK)
        text_rect = no_event_text.get_rect(center=(event_x + event_width // 2, content_y + content_height // 2))
        screen.blit(no_event_text, text_rect)
    else:
        # アクティブイベント一覧
        for i, event in enumerate(all_active_events):
            # イベント名
            event_name_text = small_font.render(event["name"], True, BLACK)
            screen.blit(event_name_text, (event_x + 5, content_y + 5 + i * 50))
            
            # イベントタイプを色で区別（外部要因は青、内部要因はオレンジ）
            event_type_color = AWS_BLUE if "duration" in event else AWS_ORANGE
            event_type_text = small_font.render("外部" if "duration" in event else "内部", True, event_type_color)
            screen.blit(event_type_text, (event_x + event_width - 30, content_y + 5 + i * 50))
            
            # 効果
            if "effect" in event:
                effect = event["effect"]
                effect_color = AWS_GREEN if "+" in effect else (255, 0, 0)
                effect_text = small_font.render(f"効果: {effect}", True, effect_color)
                screen.blit(effect_text, (event_x + 10, content_y + 25 + i * 50))
            
            # 残りターン数
            if "remaining_turns" in event:
                remaining_text = small_font.render(f"残り: {event['remaining_turns']}ターン", True, BLACK)
                screen.blit(remaining_text, (event_x + 10, content_y + 45 + i * 50))
            
            # 区切り線
            if i < len(all_active_events) - 1:
                pygame.draw.line(screen, GRAY, 
                                (event_x + 5, content_y + 65 + i * 50),
                                (event_x + event_width - 5, content_y + 65 + i * 50), 1)
            
            # 最大3つまで表示
            if i >= 2:
                if len(all_active_events) > 3:
                    more_text = small_font.render(f"...他 {len(all_active_events) - 3} イベント", True, BLACK)
                    screen.blit(more_text, (event_x + 5, content_y + 70 + 2 * 50))
                break
# クレジット履歴のチャートを描画
def draw_credit_chart():
    # チャートの背景 - 画面最上部に横いっぱいに配置
    chart_x = 20
    chart_y = 20  # 最上部に配置
    chart_width = SCREEN_WIDTH - 40  # 画面幅いっぱい（左右に少し余白）
    
    # チャートの余白を設定
    margin = 60  # 左右と上下の余白を増やす
    
    pygame.draw.rect(screen, WHITE, (chart_x, chart_y, chart_width, chart_height))
    pygame.draw.rect(screen, BLACK, (chart_x, chart_y, chart_width, chart_height), 2)
    
    # チャートのタイトルを中央上部に配置
    title_text = normal_font.render("クレジット推移", True, BLACK)
    title_rect = title_text.get_rect(center=(chart_x + chart_width // 2, chart_y + 20))
    screen.blit(title_text, title_rect)
    
    # 軸の描画
    axis_color = BLACK
    pygame.draw.line(screen, axis_color, (chart_x + margin, chart_y + 30), (chart_x + margin, chart_y + chart_height - margin/2), 2)  # Y軸
    pygame.draw.line(screen, axis_color, (chart_x + margin, chart_y + chart_height - margin/2), (chart_x + chart_width - margin/2, chart_y + chart_height - margin/2), 2)  # X軸
    
    # 最大値を計算
    max_credit = 20  # 初期値
    for player in players:
        if player.credit_history:
            player_max = max(player.credit_history)
            if player_max > max_credit:
                max_credit = player_max
    
    # スケールの調整
    y_scale = (chart_height - margin) / max(max_credit, 1)
    
    # 各プレイヤーの折れ線グラフを描画
    for i, player in enumerate(players):
        if len(player.credit_history) < 2:
            continue
            
        # 折れ線グラフの描画
        points = []
        for t, credit in enumerate(player.credit_history):
            x = chart_x + margin + t * (chart_width - margin*1.5) / max(len(player.credit_history) - 1, 1)
            y = chart_y + chart_height - margin/2 - credit * y_scale
            points.append((x, y))
            
        if len(points) >= 2:
            pygame.draw.lines(screen, player.color, False, points, 3)
            
        # 最新の値にマーカーを表示
        if points:
            pygame.draw.circle(screen, player.color, points[-1], 5)
            value_text = small_font.render(str(player.credits), True, player.color)
            # 値が画面外にはみ出さないように位置を調整
            text_x = min(points[-1][0] + 5, chart_x + chart_width - 30)
            text_y = max(points[-1][1] - 15, chart_y + 15)
            screen.blit(value_text, (text_x, text_y))
    
    # 目盛りの追加
    # Y軸の目盛り
    tick_count = 5  # 目盛りの数
    for i in range(tick_count + 1):
        tick_value = max_credit * i // tick_count
        tick_y = chart_y + chart_height - margin/2 - tick_value * y_scale
        pygame.draw.line(screen, axis_color, (chart_x + margin - 5, tick_y), (chart_x + margin, tick_y), 1)
        tick_text = small_font.render(str(tick_value), True, BLACK)
        screen.blit(tick_text, (chart_x + margin - 30, tick_y - 8))

# 現在のプレイヤーを強調表示するバナー
def draw_current_player_banner():
    current_player = players[current_player_index]
    
    # 画面上部に大きなバナーを表示
    banner_height = 60
    banner_y = chart_height + 10  # チャートの下に配置
    
    # バナーの背景（現在のプレイヤーの色で塗る）
    pygame.draw.rect(screen, current_player.color, (0, banner_y, SCREEN_WIDTH, banner_height))
    pygame.draw.rect(screen, BLACK, (0, banner_y, SCREEN_WIDTH, banner_height), 2)
    
    # 中央に大きなテキストで現在のプレイヤー名を表示
    player_text = title_font.render(f"{current_player.name}のターン", True, WHITE)
    text_rect = player_text.get_rect(center=(SCREEN_WIDTH // 2, banner_y + banner_height // 2))
    screen.blit(player_text, text_rect)
    
    # ターン数も表示
    turn_text = normal_font.render(f"ターン {turn_count}/{max_turns}", True, WHITE)
    turn_rect = turn_text.get_rect(right=SCREEN_WIDTH - 20, centery=banner_y + banner_height // 2)
    screen.blit(turn_text, turn_rect)
    
    return banner_y + banner_height  # 次の要素の開始Y座標を返す

# ターン開始時のランダムイベント発生チェック
def check_random_event(player):
    # 20%の確率でランダムイベント発生
    if random.random() < 0.2:
        random_event = generate_random_event()
        apply_event_effect(player, random_event)
        return random_event
    return None

# ゲーム状態に応じてボタンの有効/無効を更新する関数
def update_button_states():
    # サイコロボタンはROLL状態の時のみ有効
    roll_button.enabled = (game_state == "ROLL")
    
    # サービス導入ボタンはSERVICE状態かつサービスカードがある時のみ有効
    buy_button.enabled = (game_state == "SERVICE" and current_service is not None and 
                         players[current_player_index].credits >= current_service["cost"])
    
    # スキップボタンはSERVICEまたはEVENT状態の時のみ有効
    skip_button.enabled = (game_state == "SERVICE" or game_state == "EVENT")
    
    # アクションボタンはROLL状態の時のみ有効（他プレイヤーがいる場合）
    action_button.enabled = (game_state == "ROLL" and len(players) > 1)
# メインゲームループ
running = True
clock = pygame.time.Clock()

while running:
    mouse_pos = pygame.mouse.get_pos()
    
    # ゲーム状態に応じてボタンの有効/無効を更新
    update_button_states()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        
        if game_state == "ROLL":
            if roll_button.is_clicked(mouse_pos, event):
                current_player = players[current_player_index]
                
                # ターン開始時に収入を得る
                if current_player.skip_turn:
                    current_player.skip_turn = False
                    game_state = "ROLL"
                    current_player_index = (current_player_index + 1) % len(players)
                    if current_player_index == 0:
                        turn_count += 1
                        winner = check_winner()
                        if winner or turn_count > max_turns:
                            game_state = "END"
                else:
                    # 収入を得る
                    apply_turn_revenue(current_player)
                    
                    # ターン開始時にランダムイベントが発生する可能性をチェック
                    random_event = check_random_event(current_player)
                    if random_event:
                        current_event = random_event
                        game_state = "EVENT"
                    else:
                        dice_value = roll_dice()
                        current_player.position = (current_player.position + dice_value) % board_positions
                        
                        # マスの種類によってゲーム状態を変更
                        if current_player.position % 3 == 0:  # サービスマス
                            if service_deck:
                                current_service = service_deck.pop()
                                current_event = None
                                game_state = "SERVICE"
                            else:
                                game_state = "ROLL"
                                current_player_index = (current_player_index + 1) % len(players)
                                if current_player_index == 0:
                                    turn_count += 1
                                    winner = check_winner()
                                    if winner or turn_count > max_turns:
                                        game_state = "END"
                        
                        elif current_player.position % 3 == 1:  # イベントマス
                            # イベント発生確率（80%）
                            event_chance = 0.8
                            if random.random() < event_chance:
                                # 50%の確率で既存イベントから選択、50%の確率で動的生成
                                if random.random() < 0.5 and events:
                                    # 既存イベントからランダムに選択
                                    current_event = random.choice(events)
                                else:
                                    # 動的にイベントを生成
                                    current_event = generate_random_event()
                                
                                current_service = None
                                apply_event_effect(current_player, current_event)
                                game_state = "EVENT"
                            else:
                                # イベントが発生しない場合
                                current_event = None
                                game_state = "ROLL"
                                current_player_index = (current_player_index + 1) % len(players)
                                if current_player_index == 0:
                                    turn_count += 1
                                    winner = check_winner()
                                    if winner or turn_count > max_turns:
                                        game_state = "END"
                        
                        elif current_player.position % 3 == 2:  # 通常マス
                            # 通常マスでも30%の確率でイベント発生
                            normal_event_chance = 0.3
                            if random.random() < normal_event_chance:
                                # イベント発生
                                if random.random() < 0.5 and events:
                                    current_event = random.choice(events)
                                else:
                                    current_event = generate_random_event()
                                current_service = None
                                apply_event_effect(current_player, current_event)
                                game_state = "EVENT"
                            else:
                                # イベントが発生しない場合
                                current_service = None
                                current_event = None
                                game_state = "ROLL"
                                current_player_index = (current_player_index + 1) % len(players)
                                if current_player_index == 0:
                                    turn_count += 1
                                    winner = check_winner()
                                    if winner or turn_count > max_turns:
                                        game_state = "END"
            
            # アクションボタンのクリック処理
            elif action_button.is_clicked(mouse_pos, event):
                game_state = "ACTION"  # アクション選択画面へ
        
        elif game_state == "SERVICE":
            current_player = players[current_player_index]
            
            if buy_button.is_clicked(mouse_pos, event):
                if current_player.credits >= current_service["cost"]:
                    current_player.services.append(current_service)
                    current_player.credits -= current_service["cost"]
                    current_player.update_credit_history()  # クレジット履歴を更新
                    
                    current_service = None
                    game_state = "ROLL"
                    current_player_index = (current_player_index + 1) % len(players)
                    if current_player_index == 0:
                        turn_count += 1
                        winner = check_winner()
                        if winner or turn_count > max_turns:
                            game_state = "END"
            
            elif skip_button.is_clicked(mouse_pos, event):
                current_service = None
                game_state = "ROLL"
                current_player_index = (current_player_index + 1) % len(players)
                if current_player_index == 0:
                    turn_count += 1
                    winner = check_winner()
                    if winner or turn_count > max_turns:
                        game_state = "END"
        
        elif game_state == "EVENT":
            if skip_button.is_clicked(mouse_pos, event):
                current_event = None
                game_state = "ROLL"
                current_player_index = (current_player_index + 1) % len(players)
                if current_player_index == 0:
                    turn_count += 1
                    winner = check_winner()
                    if winner or turn_count > max_turns:
                        game_state = "END"
        
        elif game_state == "ACTION":
            # アクション選択画面の処理
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                # キャンセルボタンのクリック処理
                if cancel_button.collidepoint(mouse_pos):
                    game_state = "ROLL"  # アクション選択をキャンセル
                
                # アクションボタンのクリック処理
                for button_rect, action in action_buttons:
                    if button_rect.collidepoint(mouse_pos):
                        current_action = action
                        game_state = "TARGET"  # ターゲット選択画面へ
                        break
        
        elif game_state == "TARGET":
            # ターゲット選択画面の処理
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                # キャンセルボタンのクリック処理
                if cancel_button.collidepoint(mouse_pos):
                    game_state = "ACTION"  # アクション選択画面に戻る
                
                # ターゲットボタンのクリック処理
                for button_rect, target_player in target_buttons:
                    if button_rect.collidepoint(mouse_pos):
                        # アクションを実行
                        result_message = execute_player_action(current_action, players[current_player_index], target_player)
                        game_state = "ACTION_RESULT"  # 結果表示画面へ
                        break
        
        elif game_state == "ACTION_RESULT":
            # アクション結果画面の処理
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if ok_button and ok_button.collidepoint(mouse_pos):
                    game_state = "ROLL"  # ゲームに戻る
    
    # 画面の描画
    screen.fill(WHITE)
    
    # クレジットチャートを描画（最上部）
    draw_credit_chart()
    
    # 現在のプレイヤーを強調表示するバナー
    banner_bottom = draw_current_player_banner()
    
    # 左右の区切り線を描画
    pygame.draw.line(screen, BLACK, (SCREEN_WIDTH // 2, banner_bottom), (SCREEN_WIDTH // 2, SCREEN_HEIGHT), 2)
    
    # ボードとプレイヤーの描画（左側）
    draw_board()
    draw_players()
    draw_dice()  # サイコロを描画
    
    # 右側の情報パネル
    draw_game_info()
    next_panel_y = draw_player_info()  # プレイヤー情報パネルの下端のY座標を取得
    
    # 現在のプレイヤーのサービス一覧を表示
    if game_state != "END":
        draw_services_and_events(players[current_player_index])
    
    # カード情報を描画
    draw_card_info()
    
    # アクション関連の画面を描画
    if game_state == "ACTION":
        # アクション選択画面の描画
        from player_actions_ui import draw_action_selection
        action_buttons, cancel_button = draw_action_selection(screen, normal_font, small_font, players[current_player_index], SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, AWS_BLUE, AWS_ORANGE)
    
    elif game_state == "TARGET":
        # ターゲット選択画面の描画
        from player_actions_ui import draw_target_selection
        target_buttons, cancel_button = draw_target_selection(screen, normal_font, small_font, players[current_player_index], players, current_action, SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE)
    
    elif game_state == "ACTION_RESULT":
        # アクション結果画面の描画
        from player_actions_ui import draw_action_result
        ok_button = draw_action_result(screen, normal_font, result_message, SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, AWS_BLUE)
    
    # すべてのボタンを常に描画し、状態に応じて見た目を変える
    roll_button.check_hover(mouse_pos)
    roll_button.draw()
    
    buy_button.check_hover(mouse_pos)
    buy_button.draw()
    
    skip_button.check_hover(mouse_pos)
    skip_button.draw()
    
    action_button.check_hover(mouse_pos)
    action_button.draw()
    
    if game_state == "END":
        # ゲーム終了画面
        end_bg = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.draw.rect(screen, LIGHT_BLUE, end_bg, border_radius=10)
        pygame.draw.rect(screen, BLACK, end_bg, 3, border_radius=10)
        
        end_text = title_font.render("ゲーム終了", True, BLACK)
        end_rect = end_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 40))
        screen.blit(end_text, end_rect)
        
        # 全プレイヤーの最終結果を表示
        for i, player in enumerate(players):
            y_offset = i * 50
            result_text = normal_font.render(f"{player.name}: {player.credits} クレジット", True, player.color)
            result_rect = result_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + y_offset))
            screen.blit(result_text, result_rect)
        
        # 勝者の表示
        if winner:
            winner_text = normal_font.render(f"勝者: {winner.name}", True, winner.color)
            winner_rect = winner_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
            screen.blit(winner_text, winner_rect)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
# ターン開始時のランダムイベント発生チェック
def check_random_event(player):
    # 20%の確率でランダムイベント発生
    if random.random() < 0.2:
        random_event = generate_random_event()
        apply_event_effect(player, random_event)
        return random_event
    return None
# 現在のプレイヤーを強調表示するバナー
def draw_current_player_banner():
    current_player = players[current_player_index]
    
    # 画面上部に大きなバナーを表示
    banner_height = 60
    banner_y = chart_height + 10  # チャートの下に配置
    
    # バナーの背景（現在のプレイヤーの色で塗る）
    pygame.draw.rect(screen, current_player.color, (0, banner_y, SCREEN_WIDTH, banner_height))
    pygame.draw.rect(screen, BLACK, (0, banner_y, SCREEN_WIDTH, banner_height), 2)
    
    # 中央に大きなテキストで現在のプレイヤー名を表示
    player_text = title_font.render(f"{current_player.name}のターン", True, WHITE)
    text_rect = player_text.get_rect(center=(SCREEN_WIDTH // 2, banner_y + banner_height // 2))
    screen.blit(player_text, text_rect)
    
    # ターン数も表示
    turn_text = normal_font.render(f"ターン {turn_count}/{max_turns}", True, WHITE)
    turn_rect = turn_text.get_rect(right=SCREEN_WIDTH - 20, centery=banner_y + banner_height // 2)
    screen.blit(turn_text, turn_rect)
    
    return banner_y + banner_height  # 次の要素の開始Y座標を返す
# プレイヤー間アクションの定義
player_actions = [
    {
        "name": "技術提携",
        "description": "AWSの技術ノウハウを共有し、両社の成長を促進",
        "type": "cooperation",
        "effect": "両プレイヤーがクレジット+3を獲得",
        "cost": 2,  # アクション実行コスト
    },
    {
        "name": "共同マーケティング",
        "description": "共同でマーケティングキャンペーンを実施",
        "type": "cooperation",
        "effect": "両プレイヤーの顧客数+3",
        "cost": 2,
    },
    {
        "name": "クラウド移行支援",
        "description": "相手企業のクラウド移行を支援",
        "type": "cooperation",
        "effect": "相手プレイヤーのクレジット+4、自分は+1",
        "cost": 1,
    },
    {
        "name": "セキュリティ監査",
        "description": "相手企業のセキュリティ脆弱性を指摘",
        "type": "interference",
        "effect": "相手プレイヤーの次のターンをスキップ",
        "cost": 3,
    },
    {
        "name": "価格競争",
        "description": "低価格戦略で市場シェアを奪う",
        "type": "interference",
        "effect": "相手プレイヤーの顧客数-3、自分の顧客数+1",
        "cost": 3,
    },
    {
        "name": "人材引き抜き",
        "description": "相手企業から優秀なエンジニアを引き抜く",
        "type": "interference",
        "effect": "相手プレイヤーのクレジット-2、自分のクレジット+1",
        "cost": 2,
    },
]

# プレイヤー間アクションを実行する関数
def execute_player_action(action, source_player, target_player):
    # アクションコストを支払う
    source_player.credits -= action["cost"]
    
    # アクション効果を適用
    if action["name"] == "技術提携":
        source_player.credits += 3
        target_player.credits += 3
        source_player.update_credit_history()
        target_player.update_credit_history()
        return f"{source_player.name}と{target_player.name}が技術提携！両社がクレジット+3を獲得"
        
    elif action["name"] == "共同マーケティング":
        source_player.customers += 3
        target_player.customers += 3
        source_player.update_customer_history()
        target_player.update_customer_history()
        return f"{source_player.name}と{target_player.name}が共同マーケティングを実施！両社の顧客数+3"
        
    elif action["name"] == "クラウド移行支援":
        source_player.credits += 1
        target_player.credits += 4
        source_player.update_credit_history()
        target_player.update_credit_history()
        return f"{source_player.name}が{target_player.name}のクラウド移行を支援！{target_player.name}のクレジット+4、{source_player.name}のクレジット+1"
        
    elif action["name"] == "セキュリティ監査":
        target_player.skip_turn = True
        return f"{source_player.name}が{target_player.name}にセキュリティ監査を実施！{target_player.name}の次のターンはスキップ"
        
    elif action["name"] == "価格競争":
        source_player.customers += 1
        target_player.customers -= 3
        if target_player.customers < 0:
            target_player.customers = 0
        source_player.update_customer_history()
        target_player.update_customer_history()
        return f"{source_player.name}が{target_player.name}と価格競争！{target_player.name}の顧客数-3、{source_player.name}の顧客数+1"
        
    elif action["name"] == "人材引き抜き":
        source_player.credits += 1
        target_player.credits -= 2
        if target_player.credits < 0:
            target_player.credits = 0
        source_player.update_credit_history()
        target_player.update_credit_history()
        return f"{source_player.name}が{target_player.name}から人材を引き抜き！{target_player.name}のクレジット-2、{source_player.name}のクレジット+1"
    
    return "アクションを実行しました"

# プレイヤー間アクション選択画面を表示する関数
def draw_action_selection(source_player):
    # 半透明のオーバーレイ
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    # タイトル
    title_text = title_font.render("プレイヤーアクション", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
    screen.blit(title_text, title_rect)
    
    # 説明
    desc_text = normal_font.render("他のプレイヤーに対して実行するアクションを選択してください", True, WHITE)
    desc_rect = desc_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
    screen.blit(desc_text, desc_rect)
    
    # 現在のクレジット表示
    credit_text = normal_font.render(f"現在のクレジット: {source_player.credits}", True, WHITE)
    credit_rect = credit_text.get_rect(center=(SCREEN_WIDTH // 2, 140))
    screen.blit(credit_text, credit_rect)
    
    # アクションカードの表示
    card_width = 200
    card_height = 150
    cards_per_row = 3
    margin_x = 50
    margin_y = 30
    start_y = 180
    
    action_buttons = []
    
    for i, action in enumerate(player_actions):
        row = i // cards_per_row
        col = i % cards_per_row
        
        card_x = (SCREEN_WIDTH - (card_width * cards_per_row + margin_x * (cards_per_row - 1))) // 2 + col * (card_width + margin_x)
        card_y = start_y + row * (card_height + margin_y)
        
        # カードの背景色（協力は青、妨害はオレンジ）
        card_color = AWS_BLUE if action["type"] == "cooperation" else AWS_ORANGE
        
        # カードの描画
        pygame.draw.rect(screen, card_color, (card_x, card_y, card_width, card_height), border_radius=10)
        pygame.draw.rect(screen, WHITE, (card_x, card_y, card_width, card_height), 2, border_radius=10)
        
        # アクション名
        name_text = normal_font.render(action["name"], True, WHITE)
        name_rect = name_text.get_rect(center=(card_x + card_width // 2, card_y + 25))
        screen.blit(name_text, name_rect)
        
        # 説明（長い場合は2行に分割）
        desc = action["description"]
        if len(desc) > 20:
            desc1 = desc[:20]
            desc2 = desc[20:]
            desc_text1 = small_font.render(desc1, True, WHITE)
            desc_text2 = small_font.render(desc2, True, WHITE)
            screen.blit(desc_text1, (card_x + 10, card_y + 50))
            screen.blit(desc_text2, (card_x + 10, card_y + 70))
        else:
            desc_text = small_font.render(desc, True, WHITE)
            screen.blit(desc_text, (card_x + 10, card_y + 60))
        
        # 効果
        effect_text = small_font.render(action["effect"], True, WHITE)
        screen.blit(effect_text, (card_x + 10, card_y + 95))
        
        # コスト
        cost_text = small_font.render(f"コスト: {action['cost']}", True, WHITE)
        screen.blit(cost_text, (card_x + 10, card_y + 120))
        
        # 選択可能かどうか（コストが支払えるか）
        if source_player.credits >= action["cost"]:
            # 選択可能なカードはボタンとして登録
            action_buttons.append((pygame.Rect(card_x, card_y, card_width, card_height), action))
        else:
            # 選択不可能なカードは暗く表示
            disabled_overlay = pygame.Surface((card_width, card_height))
            disabled_overlay.set_alpha(150)
            disabled_overlay.fill(BLACK)
            screen.blit(disabled_overlay, (card_x, card_y))
            
            unavailable_text = small_font.render("クレジット不足", True, (255, 100, 100))
            unavailable_rect = unavailable_text.get_rect(center=(card_x + card_width // 2, card_y + card_height - 20))
            screen.blit(unavailable_text, unavailable_rect)
    
    # キャンセルボタン
    cancel_button_width = 150
    cancel_button_height = 50
    cancel_button_x = (SCREEN_WIDTH - cancel_button_width) // 2
    cancel_button_y = SCREEN_HEIGHT - 100
    
    cancel_button = pygame.Rect(cancel_button_x, cancel_button_y, cancel_button_width, cancel_button_height)
    pygame.draw.rect(screen, GRAY, cancel_button, border_radius=5)
    pygame.draw.rect(screen, WHITE, cancel_button, 2, border_radius=5)
    
    cancel_text = normal_font.render("キャンセル", True, WHITE)
    cancel_rect = cancel_text.get_rect(center=cancel_button.center)
    screen.blit(cancel_text, cancel_rect)
    
    return action_buttons, cancel_button

# ターゲットプレイヤー選択画面を表示する関数
def draw_target_selection(source_player, action):
    # 半透明のオーバーレイ
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    # タイトル
    title_text = title_font.render(f"{action['name']}", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
    screen.blit(title_text, title_rect)
    
    # 説明
    desc_text = normal_font.render("アクションの対象となるプレイヤーを選択してください", True, WHITE)
    desc_rect = desc_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
    screen.blit(desc_text, desc_rect)
    
    # プレイヤーカードの表示
    card_width = 250
    card_height = 150
    margin = 50
    
    target_buttons = []
    
    # 自分以外のプレイヤーを表示
    available_targets = [p for p in players if p != source_player]
    
    for i, player in enumerate(available_targets):
        # カードの位置を計算（中央に配置）
        total_width = len(available_targets) * card_width + (len(available_targets) - 1) * margin
        start_x = (SCREEN_WIDTH - total_width) // 2
        
        card_x = start_x + i * (card_width + margin)
        card_y = SCREEN_HEIGHT // 2 - card_height // 2
        
        # カードの描画
        pygame.draw.rect(screen, player.color, (card_x, card_y, card_width, card_height), border_radius=10)
        pygame.draw.rect(screen, WHITE, (card_x, card_y, card_width, card_height), 2, border_radius=10)
        
        # プレイヤー名
        name_text = normal_font.render(player.name, True, WHITE)
        name_rect = name_text.get_rect(center=(card_x + card_width // 2, card_y + 30))
        screen.blit(name_text, name_rect)
        
        # クレジット
        credit_text = normal_font.render(f"クレジット: {player.credits}", True, WHITE)
        credit_rect = credit_text.get_rect(center=(card_x + card_width // 2, card_y + 70))
        screen.blit(credit_text, credit_rect)
        
        # 顧客数
        customer_text = normal_font.render(f"顧客数: {player.customers}", True, WHITE)
        customer_rect = customer_text.get_rect(center=(card_x + card_width // 2, card_y + 110))
        screen.blit(customer_text, customer_rect)
        
        # ボタンとして登録
        target_buttons.append((pygame.Rect(card_x, card_y, card_width, card_height), player))
    
    # キャンセルボタン
    cancel_button_width = 150
    cancel_button_height = 50
    cancel_button_x = (SCREEN_WIDTH - cancel_button_width) // 2
    cancel_button_y = SCREEN_HEIGHT - 100
    
    cancel_button = pygame.Rect(cancel_button_x, cancel_button_y, cancel_button_width, cancel_button_height)
    pygame.draw.rect(screen, GRAY, cancel_button, border_radius=5)
    pygame.draw.rect(screen, WHITE, cancel_button, 2, border_radius=5)
    
    cancel_text = normal_font.render("キャンセル", True, WHITE)
    cancel_rect = cancel_text.get_rect(center=cancel_button.center)
    screen.blit(cancel_text, cancel_rect)
    
    return target_buttons, cancel_button

# アクション結果表示画面
def draw_action_result(result_message):
    # 半透明のオーバーレイ
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    # 結果メッセージ表示用のパネル
    panel_width = 600
    panel_height = 200
    panel_x = (SCREEN_WIDTH - panel_width) // 2
    panel_y = (SCREEN_HEIGHT - panel_height) // 2
    
    pygame.draw.rect(screen, AWS_BLUE, (panel_x, panel_y, panel_width, panel_height), border_radius=10)
    pygame.draw.rect(screen, WHITE, (panel_x, panel_y, panel_width, panel_height), 2, border_radius=10)
    
    # タイトル
    title_text = normal_font.render("アクション結果", True, WHITE)
    title_rect = title_text.get_rect(center=(panel_x + panel_width // 2, panel_y + 40))
    screen.blit(title_text, title_rect)
    
    # 結果メッセージ
    result_text = normal_font.render(result_message, True, WHITE)
    result_rect = result_text.get_rect(center=(panel_x + panel_width // 2, panel_y + 100))
    screen.blit(result_text, result_rect)
    
    # OKボタン
    ok_button_width = 100
    ok_button_height = 40
    ok_button_x = panel_x + (panel_width - ok_button_width) // 2
    ok_button_y = panel_y + panel_height - 60
    
    ok_button = pygame.Rect(ok_button_x, ok_button_y, ok_button_width, ok_button_height)
    pygame.draw.rect(screen, GRAY, ok_button, border_radius=5)
    pygame.draw.rect(screen, WHITE, ok_button, 2, border_radius=5)
    
    ok_text = normal_font.render("OK", True, WHITE)
    ok_rect = ok_text.get_rect(center=ok_button.center)
    screen.blit(ok_text, ok_rect)
    
    return ok_button
