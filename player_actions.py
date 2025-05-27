# プレイヤー間アクションの定義
player_actions = [
    {
        "name": "クラウド移行支援",
        "description": "相手企業のクラウド移行を支援",
        "type": "cooperation",
        "effect": "自分+5、相手+2クレジット",
        "cost": 3,  # アクション実行コスト
    },
    {
        "name": "共同マーケティング",
        "description": "共同キャンペーンを実施",
        "type": "cooperation",
        "effect": "両プレイヤーの顧客数+3",
        "cost": 2,
    },
    {
        "name": "サービス連携",
        "description": "両社のサービスを連携",
        "type": "cooperation",
        "effect": "自分の収入+2、相手+1",
        "cost": 4,
        "revenue_boost": True,
    },
    {
        "name": "価格競争",
        "description": "低価格戦略で市場獲得",
        "type": "interference",
        "effect": "相手-3、自分+2顧客",
        "cost": 3,
    },
    {
        "name": "人材引き抜き",
        "description": "優秀なエンジニアを獲得",
        "type": "interference",
        "effect": "相手-2、自分+1収入",
        "cost": 5,
        "revenue_reduction": True,
    },
    {
        "name": "マーケティング攻勢",
        "description": "大規模キャンペーン実施",
        "type": "interference",
        "effect": "相手の顧客獲得を阻害",
        "cost": 4,
        "block_customer": True,
    },
]

# プレイヤー間アクションを実行する関数
def execute_player_action(action, source_player, target_player):
    # アクションコストを支払う
    source_player.credits -= action["cost"]
    
    # アクション効果を適用
    if action["name"] == "クラウド移行支援":
        source_player.credits += 5
        target_player.credits += 2
        return f"クラウド移行支援：両社がクレジット獲得"
        
    elif action["name"] == "共同マーケティング":
        source_player.customers += 3
        target_player.customers += 3
        source_player.update_customer_history()
        target_player.update_customer_history()
        return f"共同マーケティング：両社の顧客数+3"
        
    elif action["name"] == "サービス連携":
        # 収入増加の効果を適用（サービスの収益を直接増加）
        for service in source_player.services:
            service["revenue"] += 2
        for service in target_player.services:
            service["revenue"] += 1
        return f"サービス連携：収入が増加"
        
    elif action["name"] == "価格競争":
        source_player.customers += 2
        target_player.customers -= 3
        if target_player.customers < 0:
            target_player.customers = 0
        source_player.update_customer_history()
        target_player.update_customer_history()
        return f"価格競争：顧客の移動が発生"
    
    elif action["name"] == "人材引き抜き":
        # 収入減少の効果を適用（サービスの収益を直接減少）
        for service in target_player.services:
            service["revenue"] = max(1, service["revenue"] - 2)  # 最低1は保証
        for service in source_player.services:
            service["revenue"] += 1
        return f"人材引き抜き：収入に変化"
    
    elif action["name"] == "マーケティング攻勢":
        # 顧客獲得阻害の効果を適用（3ターン続く効果）
        target_player.active_internal_events.append({
            "name": "マーケティング攻勢の影響",
            "type": "customer_block",
            "remaining_turns": 3,
            "effect": "顧客獲得-50%"
        })
        return f"{source_player.name}がマーケティング攻勢！{target_player.name}の顧客獲得が3ターン阻害される"
    
    return "アクションを実行しました"
