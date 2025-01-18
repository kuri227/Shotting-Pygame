import random as r
import pygame as pg


chip_s = 48
map_s = pg.Vector2(16, 9)
disp_w = int(chip_s * map_s.x)
disp_h = int(chip_s * map_s.y)
bow_hp = 3


class Arrow:  # 矢に関するクラス
  def __init__(self, x, y, velocity):
    self.position = pg.Vector2(x * chip_s, y * chip_s)
    self.velocity = velocity
    self.size = pg.Vector2(48, 48)

  def updata(self):  # 位置の更新
    self.position += self.velocity

  def is_off_screen(self, screen_height):  # 描画有効範囲に関する設定
    return screen_height - self.position.y + 10 < 0

  def collide(self, rect):
    arrow_rect = pg.Rect(self.position.x, self.position.y,
                         self.size.x, self.size.y)
    return arrow_rect.colliderect(rect)

class Ball:  # ボールに関するクラス
  def __init__(self, x, y, radius, v_x, v_y):
    self.position = pg.Vector2(x, y)
    self.velocity = pg.Vector2(v_x, v_y)
    self.acceleration = pg.Vector2(0, 0.98)
    self.size = pg.Vector2(radius * 2, radius * 2)
    self.radius = radius
    self.hp = r.randint(3, 5)
    self.initial_hp = self.hp

  def updata(self):  # 位置、速度の更新
    self.position += self.velocity
    self.velocity += self.acceleration

  def collide(self, rect):
    ball_rect = pg.Rect(self.position.x - self.radius, self.position.y - self.radius,
                        self.size.x, self.size.y)
    return ball_rect.colliderect(rect)

# スタート画面の表示
def show_start_menu(screen, font):
  screen.fill(pg.Color('WHITE'))
  menu_text = font.render("スペースキーを押してスタート！！", True, "BLACK")
  screen.blit(menu_text, (disp_w // 2 -
              menu_text.get_width() // 2, disp_h // 2))
  pg.display.update()

  # スタート画面での待機
  waiting = True
  while waiting:
    for event in pg.event.get():
      if event.type == pg.QUIT:
        return False
      if event.type == pg.KEYDOWN:
        if event.key == pg.K_SPACE:
          waiting = False
  return True


# ゲームオーバー画面の表示
def show_game_over_screen(screen, font, score):
  screen.fill(pg.Color('WHITE'))
  game_over_text = font.render("ゲームオーバー！！", True, "RED")
  score_text = font.render(f"最終スコア: {score}", True, "BLACK")
  restart_text = font.render("スペースキーを押して再プレイ", True, "BLACK")

  screen.blit(game_over_text, (disp_w // 2 -
              game_over_text.get_width() // 2, disp_h // 4))
  screen.blit(score_text, (disp_w // 2 -
              score_text.get_width() // 2, disp_h // 2))
  screen.blit(restart_text, (disp_w // 2 -
              restart_text.get_width() // 2, disp_h * 3 // 4))

  pg.display.update()

  # ゲームオーバー画面での待機
  waiting = True
  while waiting:
    for event in pg.event.get():
      if event.type == pg.QUIT:
        return False
      if event.type == pg.KEYDOWN:
        if event.key == pg.K_SPACE:
          waiting = False
  return True

# ゲームクリア画面
def show_game_clear_screen(screen, font, score):
  screen.fill(pg.Color('WHITE'))
  game_clear_text = font.render("ゲームクリア！！", True, "GREEN")
  score_text = font.render(f"最終スコア: {score}", True, "BLACK")
  hp_text = font.render(f"クリア時のあなたのHP: {bow_hp}", True, "BLACK")
  restart_text = font.render("スペースキーを押して再プレイ", True, "BLACK")

  screen.blit(game_clear_text, (disp_w // 2 -
              game_clear_text.get_width() // 2, disp_h // 4))
  screen.blit(score_text, (disp_w // 2 -
              score_text.get_width() // 2, disp_h // 2))
  screen.blit(hp_text, (disp_w // 2 -
              hp_text.get_width() // 2, disp_h // 2 + 20))
  screen.blit(restart_text, (disp_w // 2 -
              restart_text.get_width() // 2, disp_h * 3 // 4))

  pg.display.update()

  # ゲームクリア画面での待機
  waiting = True
  while waiting:
    for event in pg.event.get():
      if event.type == pg.QUIT:
        return False
      if event.type == pg.KEYDOWN:
        if event.key == pg.K_SPACE:
          waiting = False
  return True

def main():

  # 初期化処理
  pg.init()
  pg.display.set_caption('シューティングゲーム')
  disp_w = int(chip_s * map_s.x)
  disp_h = int(chip_s * map_s.y)
  screen = pg.display.set_mode((disp_w, disp_h))
  clock = pg.time.Clock()
  font = pg.font.Font("ipaexg.ttf", 15)

  while True:
    score = 0     # 得点カウントのための変数
    ball_spawn_timer = 0  # ボール再スポーンまでの時間をカウントする変数
    ball_increase_timer = 0  # ボールの出現個数を増やすためのタイマー
    # frame = 0
    exit_flag = False

    # スタート画面
    if not show_start_menu(screen, font):
      pg.quit()
      return "001"

    # グリッド設定
    # grid_c = "#bbbbbb"

    # 自キャラ移動関連のパラメータ設定
    cmd_move = -1  # 移動コマンドの管理変数
    m_vec = [pg.Vector2(1, 0), pg.Vector2(-1, 0)]  # 移動コマンドに対応したXYの移動量

  # 弓の画像読み込み、表示設定
    bow_hp = 3
    bow_p = pg.Vector2(5, 3)  # 位置
    bow_s = pg.Vector2(48, 48)  # サイズ
    damage = 0  # 無敵時間のカウント変数
    bow_img = pg.image.load(f'data/img/bow.png')  # 画像の読み込み
    bow_img = pg.transform.rotozoom(bow_img, 45, 1)  # 画像を上向きに
    bow_img = pg.transform.scale(bow_img, (chip_s, chip_s))  # 画像を(48,48)に加工

  # 矢の画像読み込み、表示設定
    arrows = []  # 矢を管理するためのリスト
    arrow_img = pg.image.load(f"data/img/arrow.png")  # 画像の読み込み
    arrow_img = pg.transform.rotozoom(arrow_img, -45, 1)  # 画像を上向きに
    arrow_img = pg.transform.scale(arrow_img, (chip_s, chip_s))  # 画像を(48,48)に加工

  # ボールリストと初期化
    balls = [Ball(50, 20, 24, 3, 2)]

  # 地面の画像読み込み、表示設定
    ground_img = pg.image.load(f'data/img/map_ground_renga.png')  # 画像読み込み
    ground_s = pg.Vector2(48, 48)

    while not exit_flag:

      # システムイベントの検出
      cmd_move = -1
      for event in pg.event.get():
        if event.type == pg.QUIT:  # ウィンドウ[X]の押下
          exit_flag = True
          exit_code = '001'
        if event.type == pg.KEYDOWN:
          if event.key == pg.K_RIGHT:  # →が押されたとき
            cmd_move = 0
          elif event.key == pg.K_LEFT:  # ←が押されたとき
            cmd_move = 1
          elif event.key == pg.K_SPACE:  # スペースキーで矢を発射
            # 速度(0,15)の矢を出現させる
            arrows.append(Arrow(bow_p.x, bow_p.y + 0, pg.Vector2(0, 15)))
          elif event.key == pg.K_0:  # テストプレイのためのコマンド
            bow_hp = 999

      # 背景描画
      screen.fill(pg.Color('WHITE'))

      # グリッド
      # for x in range(0, disp_w, chip_s):  # 縦線
      #   pg.draw.line(screen, grid_c, (x, 0), (x, disp_h))
      # for y in range(0, disp_h, chip_s):  # 横線
      #   pg.draw.line(screen, grid_c, (0, y), (disp_w, y))

      # 移動コマンドの処理
      if cmd_move != -1:
        af_pos = bow_p + m_vec[cmd_move]
        if (0 <= af_pos.x <= map_s.x - 1) and (0 <= af_pos.y <= map_s.y - 1):
          bow_p += m_vec[cmd_move]  # 画面内に収まるならキャラ座標を実際に更新

      # 矢の更新処理
      for arrow in arrows[:]:
        arrow.updata()  # 矢の位置を更新
        if arrow.is_off_screen(disp_h):
          arrows.remove(arrow)  # 描画有効範囲外にいるなら矢を消去

      # ボールの出現に関する設定
      ball_spawn_timer += clock.get_time()
      ball_increase_timer += clock.get_time()
      if ball_increase_timer <= 20000:  # ゲーム開始から20秒以内
        if ball_spawn_timer >= 5000:  # 前にボールが出現してから5秒以上
          ball_spawn_timer = 0
          new_ball = Ball(r.randint(0, int(map_s.x) - 1) * chip_s,  # 位置のx座標は画面内でランダム
                          20, 24, r.randint(3, 6), 2)  # 速度のx成分は3~6の間でランダム
          balls.append(new_ball)  # 新しくボールを作成する

      elif ball_increase_timer <= 30000:  # ゲーム開始から30秒以内
        if ball_spawn_timer >= 4000:  # 前にボールが出現してから4秒以上
          ball_spawn_timer = 0
          new_ball = Ball(r.randint(0, int(map_s.x) - 1) * chip_s,
                          20, 24, r.randint(3, 8), 2)  # 速度のx成分は3~8の間でランダム
          balls.append(new_ball)

      elif ball_increase_timer <= 40000:  # ゲーム開始から40秒以内
        if ball_spawn_timer >= 3000:  # 前にボールが出現してから3秒以上
          ball_spawn_timer = 0
          new_ball = Ball(r.randint(0, int(map_s.x) - 1) * chip_s,
                          20, 24, r.randint(3, 8), 2)
          balls.append(new_ball)

      elif ball_increase_timer <= 50000:  # ゲーム開始から50秒以内
        if ball_spawn_timer >= 2500:  # 前にボールが出現してから2.5秒以上
          ball_spawn_timer = 0
          new_ball = Ball(r.randint(0, int(map_s.x) - 1) * chip_s,
                          20, 24, r.randint(3, 8), 2)
          balls.append(new_ball)

      elif ball_increase_timer <= 60000:  # ゲーム開始から60秒以内
        if ball_spawn_timer >= 2000:  # 前にボールが出現してから2秒以上
          ball_spawn_timer = 0
          new_ball = Ball(r.randint(0, int(map_s.x) - 1) * chip_s,
                          20, 24, r.randint(3, 8), 2)
          balls.append(new_ball)

      # ボールの更新処理と描画
      for ball in balls:
        ball.updata()  # ボールの位置、速度を更新

        # 地面との衝突処理
        if ball.position.y >= disp_h - ground_s.y - ball.radius:
          ball.position.y = disp_h - ground_s.y - ball.radius
          ball.velocity.y *= -0.95
          if abs(ball.velocity.y) < 3.5:
            ball.velocity.y = 0
            ball.velocity.x *= 0.98

        # 右端と左端との衝突処理
        if ball.position.x + ball.radius > disp_w:
          ball.position.x = disp_w - ball.radius
          ball.velocity.x *= -0.95
        elif ball.position.x - ball.radius < 0:
          ball.position.x = ball.radius
          ball.velocity.x *= -0.8

        # ボールの描写
        pg.draw.circle(screen, pg.Color("#ff0000"), (int(
            ball.position.x), int(ball.position.y)), int(ball.radius), width=2)

        # ボールのhp表示
        hp_str = f"HP: {ball.hp}"
        screen.blit(font.render(hp_str, True, "BLACK"), (int(
            ball.position.x - ball.radius), int(ball.position.y - ball.radius - 10)))

      # 弓の描画
      bow_dp = pg.Vector2(bow_p.x * chip_s, disp_h - ground_s.y - chip_s)
      screen.blit(bow_img, bow_dp)

      # 矢の描画
      for arrow in arrows:
        arrow_dp = pg.Vector2(arrow.position.x,
                              disp_h - arrow.position.y)
        screen.blit(arrow_img, arrow_dp)

        # 矢とボールの当たり判定の検出
        for ball in balls[:]:
          ball_rect = pg.Rect(ball.position.x - ball.radius, ball.position.y - ball.radius,
                              ball.size.x, ball.size.y)  # ボールの当たり判定を作成

          arrow_rect = pg.Rect(arrow.position.x, disp_h -
                               arrow.position.y, arrow.size.x, arrow.size.y)  # 矢の当たり判定を作成

          if arrow_rect.colliderect(ball_rect):  # ボールが矢と接触したかを判定
            # print("矢がボールに当たった")
            ball.hp -= 1  # ボールの体力を減少
            score += 1  # スコアを1加算
            arrows.remove(arrow)  # 矢を消去
            if ball.hp <= 0:  # ボールのHPが0なら
              score += ball.initial_hp  # 倒したボールの総HPをスコアに加算
              balls.remove(ball)  # ボールを消去
            break

      for ball in balls[:]:
        ball_rect = pg.Rect(ball.position.x - ball.radius, ball.position.y - ball.radius,
                            ball.size.x, ball.size.y)  # ボールの当たり判定を作成

        bow_rect = pg.Rect(bow_p.x * chip_s, disp_h -
                           bow_p.y * chip_s, bow_s.x, bow_s.y)  # 弓の当たり判定を作成
        if damage == 0:  # 無敵時間がなければ
          if ball_rect.colliderect(bow_rect):  # ボールが弓と接触しているか判定
            bow_hp -= 1  # 弓のHPを1減少
            damage = 20  # 無敵時間を20フレーム付与
        else:
          damage -= 1  # 無敵時間を減少

      # 地面描画
      for x in range(0, disp_w, int(ground_s.x)):
        screen.blit(ground_img, (x, disp_h - ground_s.y))

      # 弓のHPを左上に表示
      bow_hp_str = f"HP: {bow_hp}"
      screen.blit(font.render(bow_hp_str, True, "BLACK"), (10, 50))

      # ゲーム開始からの経過時間を左上に表示
      time = ball_increase_timer // 1000
      time_str = f"Time: {time}"
      screen.blit(font.render(time_str, True, "BLACK"), (10, 10))

      # 現在の得点を左上に表示
      score_str = f"Score: {score}"
      screen.blit(font.render(score_str, True, "BLACK"), (10, 30))

      # フレームカウンタの描画
      # frame += 1
      # frm_str = f'{frame:05}'
      # screen.blit(font.render(frm_str, True, 'BLACK'), (10, 10))

      pg.display.update()
      clock.tick(30)

      # ゲームオーバー条件
      if bow_hp <= 0:  # 弓の体力が0になったら
        exit_flag = True
        if not show_game_over_screen(screen, font, score):  # ゲームオーバー画面
          pg.quit()  # [X]が押されたとき
          return "001"

      # ゲームクリアチェック
      if not balls and ball_increase_timer >= 60000:  # もしボールが存在せず、ゲームスタートから60秒経過
        exit_flag = True
        if not show_game_clear_screen(screen, font, score):  # ゲームクリア画面
          pg.quit()
          return "001"

    continue  # スタート画面に戻る（再度プレイ）

  pg.quit()
  return "000"

if __name__ == "__main__":
  code = main()
  print(f"プログラムを「コード{code}」で終了しました。")
