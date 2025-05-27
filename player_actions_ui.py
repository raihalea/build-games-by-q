import pygame
from player_actions import player_actions

# プレイヤー間アクション選択画面を表示する関数
def draw_action_selection(screen, font_normal, font_small, source_player, SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, AWS_BLUE, AWS_ORANGE):
    # 半透明のオーバーレイ
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    # タイトル
    title_text = font_normal.render("プレイヤーアクション", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
    screen.blit(title_text, title_rect)
    
    # 説明
    desc_text = font_normal.render("他のプレイヤーに対して実行するアクションを選択してください", True, WHITE)
    desc_rect = desc_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
    screen.blit(desc_text, desc_rect)
    
    # 現在のクレジット表示
    credit_text = font_normal.render(f"現在のクレジット: {source_player.credits}", True, WHITE)
    credit_rect = credit_text.get_rect(center=(SCREEN_WIDTH // 2, 140))
    screen.blit(credit_text, credit_rect)
    
    # アクションカードの表示
    card_width = 250  # カード幅を拡大
    card_height = 180  # カード高さを拡大
    cards_per_row = 2
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
        name_text = font_normal.render(action["name"], True, WHITE)
        name_rect = name_text.get_rect(center=(card_x + card_width // 2, card_y + 30))
        screen.blit(name_text, name_rect)
        
        # 説明（フォントサイズを小さくして1行に収める）
        desc_text = font_small.render(action["description"], True, WHITE)
        desc_rect = desc_text.get_rect(center=(card_x + card_width // 2, card_y + 70))
        screen.blit(desc_text, desc_rect)
        
        # 効果（フォントサイズを小さくして1行に収める）
        effect_text = font_small.render(action["effect"], True, WHITE)
        effect_rect = effect_text.get_rect(center=(card_x + card_width // 2, card_y + 110))
        screen.blit(effect_text, effect_rect)
        
        # コスト
        cost_text = font_small.render(f"コスト: {action['cost']}", True, WHITE)
        cost_rect = cost_text.get_rect(center=(card_x + card_width // 2, card_y + 150))
        screen.blit(cost_text, cost_rect)
        
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
            
            unavailable_text = font_small.render("クレジット不足", True, (255, 100, 100))
            unavailable_rect = unavailable_text.get_rect(center=(card_x + card_width // 2, card_y + card_height - 20))
            screen.blit(unavailable_text, unavailable_rect)
    
    # キャンセルボタン
    cancel_button_width = 150
    cancel_button_height = 50
    cancel_button_x = (SCREEN_WIDTH - cancel_button_width) // 2
    cancel_button_y = SCREEN_HEIGHT - 100
    
    cancel_button = pygame.Rect(cancel_button_x, cancel_button_y, cancel_button_width, cancel_button_height)
    pygame.draw.rect(screen, (150, 150, 150), cancel_button, border_radius=5)
    pygame.draw.rect(screen, WHITE, cancel_button, 2, border_radius=5)
    
    cancel_text = font_normal.render("キャンセル", True, WHITE)
    cancel_rect = cancel_text.get_rect(center=cancel_button.center)
    screen.blit(cancel_text, cancel_rect)
    
    return action_buttons, cancel_button

# ターゲットプレイヤー選択画面を表示する関数
def draw_target_selection(screen, font_normal, font_small, source_player, players, action, SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE):
    # 半透明のオーバーレイ
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    # タイトル
    title_text = font_normal.render(f"{action['name']}", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
    screen.blit(title_text, title_rect)
    
    # 説明
    desc_text = font_normal.render("アクションの対象となるプレイヤーを選択してください", True, WHITE)
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
        name_text = font_normal.render(player.name, True, WHITE)
        name_rect = name_text.get_rect(center=(card_x + card_width // 2, card_y + 30))
        screen.blit(name_text, name_rect)
        
        # クレジット
        credit_text = font_normal.render(f"クレジット: {player.credits}", True, WHITE)
        credit_rect = credit_text.get_rect(center=(card_x + card_width // 2, card_y + 70))
        screen.blit(credit_text, credit_rect)
        
        # 顧客数
        customer_text = font_normal.render(f"顧客数: {player.customers}", True, WHITE)
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
    pygame.draw.rect(screen, (150, 150, 150), cancel_button, border_radius=5)
    pygame.draw.rect(screen, WHITE, cancel_button, 2, border_radius=5)
    
    cancel_text = font_normal.render("キャンセル", True, WHITE)
    cancel_rect = cancel_text.get_rect(center=cancel_button.center)
    screen.blit(cancel_text, cancel_rect)
    
    return target_buttons, cancel_button

# アクション結果表示画面
def draw_action_result(screen, font_normal, result_message, SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, AWS_BLUE):
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
    title_text = font_normal.render("アクション結果", True, WHITE)
    title_rect = title_text.get_rect(center=(panel_x + panel_width // 2, panel_y + 40))
    screen.blit(title_text, title_rect)
    
    # 結果メッセージ
    result_text = font_normal.render(result_message, True, WHITE)
    result_rect = result_text.get_rect(center=(panel_x + panel_width // 2, panel_y + 100))
    screen.blit(result_text, result_rect)
    
    # OKボタン
    ok_button_width = 100
    ok_button_height = 40
    ok_button_x = panel_x + (panel_width - ok_button_width) // 2
    ok_button_y = panel_y + panel_height - 60
    
    ok_button = pygame.Rect(ok_button_x, ok_button_y, ok_button_width, ok_button_height)
    pygame.draw.rect(screen, (150, 150, 150), ok_button, border_radius=5)
    pygame.draw.rect(screen, WHITE, ok_button, 2, border_radius=5)
    
    ok_text = font_normal.render("OK", True, WHITE)
    ok_rect = ok_text.get_rect(center=ok_button.center)
    screen.blit(ok_text, ok_rect)
    
    return ok_button
