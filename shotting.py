import random as r
import pygame as pg


chip_s = 48
map_s = pg.Vector2(16, 9)
disp_w = int(chip_s * map_s.x)
disp_h = int(chip_s * map_s.y)
bow_hp = 3

class Arrow:
  def __init__(self, x, y, velocity):
    self.position = pg.Vector2(x * chip_s, y * chip_s)
    self.velocity = velocity
    self.size = pg.Vector2(48, 48)

  def updata(self):
    self.position += self.velocity

  def is_off_screen(self, screen_height):
    return screen_height - self.position.y + 10 < 0

  def collide(self, rect):
    arrow_rect = pg.Rect(self.position.x, self.position.y,
                         self.size.x, self.size.y)
    return arrow_rect.colliderect(rect)

class Ball:
  def __init__(self, x, y, radius):
    self.position = pg.Vector2(x, y)
    self.velocity = pg.Vector2(3, 2)
    self.acceleration = pg.Vector2(0, 0.1)
    self.size = pg.Vector2(radius * 2, radius * 2)
    self.radius = radius
    self.hp = r.randint(3, 5)
    self.initial_hp = self.hp

  def updata(self):
    self.position += self.velocity
    self.velocity += self.acceleration

  def collide(self, rect):
    ball_rect = pg.Rect(self.position.x - self.radius, self.position.y - self.radius,
                        self.size.x, self.size.y)
    return ball_rect.colliderect(rect)


# 追加する関数: メインメニュー画面の表示
def show_start_menu(screen, font):
  screen.fill(pg.Color('WHITE'))
  menu_text = font.render("Press SPACE to Start", True, "BLACK")
  screen.blit(menu_text, (disp_w // 2 -
              menu_text.get_width() // 2, disp_h // 2))
  pg.display.update()

  # メニュー画面の待機
  waiting = True
  while waiting:
    for event in pg.event.get():
      if event.type == pg.QUIT:
        return False
      if event.type == pg.KEYDOWN:
        if event.key == pg.K_SPACE:
          waiting = False
  return True


# 追加する関数: ゲームオーバー画面の表示
def show_game_over_screen(screen, font, score):
  screen.fill(pg.Color('WHITE'))
  game_over_text = font.render("Game Over", True, "RED")
  score_text = font.render(f"Final Score: {score}", True, "BLACK")
  restart_text = font.render("Press SPACE to Restart", True, "BLACK")

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

def main():

  # 初期化処理
  pg.init()
  pg.display.set_caption('シューティングゲーム')
  disp_w = int(chip_s * map_s.x)
  disp_h = int(chip_s * map_s.y)
  screen = pg.display.set_mode((disp_w, disp_h))
  clock = pg.time.Clock()
  font = pg.font.Font(None, 15)
  score = 0     # 得点カウントのための変数
  ball_spawn_timer = 0  # ボール再スポーンまでの時間をカウントする変数
  frame = 0
  exit_flag = False
  exit_code = '000'

  if not show_start_menu(screen, font):
    pg.quit()
    return "001"

  # グリッド設定
  grid_c = "#bbbbbb"

  # 自キャラ移動関連のパラメータ設定
  cmd_move = -1  # 移動コマンドの管理変数
  m_vec = [pg.Vector2(1, 0), pg.Vector2(-1, 0)]  # 移動コマンドに対応したXYの移動量

  # 弓の画像読み込み、表示設定
  bow_p = pg.Vector2(2, 3)
  bow_s = pg.Vector2(48, 48)
  bow_img = pg.image.load(f'data/img/bow.png')
  bow_img = pg.transform.rotozoom(bow_img, 45, 1)
  bow_img = pg.transform.scale(bow_img, (chip_s, chip_s))

  # 矢の画像読み込み、表示設定
  arrows = []
  arrow_img = pg.image.load(f"data/img/arrow.png")
  arrow_img = pg.transform.rotozoom(arrow_img, -45, 1)
  arrow_img = pg.transform.scale(arrow_img, (chip_s, chip_s))

  # ボールリストと初期化
  balls = [Ball(50, 20, 24)]

  # 地面の画像読み込み、表示設定
  ground_img = pg.image.load(f'data/img/map_ground_renga.png')
  ground_s = pg.Vector2(48, 48)

  while not exit_flag:

    # システムイベントの検出
    cmd_move = -1
    for event in pg.event.get():
      if event.type == pg.QUIT:  # ウィンドウ[X]の押下
        exit_flag = True
        exit_code = '001'
      if event.type == pg.KEYDOWN:
        if event.key == pg.K_RIGHT:
          cmd_move = 0
        elif event.key == pg.K_LEFT:
          cmd_move = 1
        elif event.key == pg.K_SPACE:  # スペースキーで矢を発射
          arrows.append(Arrow(bow_p.x, bow_p.y + 0, pg.Vector2(0, 15)))

    # 背景描画
    screen.fill(pg.Color('WHITE'))

    # グリッド
    for x in range(0, disp_w, chip_s):  # 縦線
      pg.draw.line(screen, grid_c, (x, 0), (x, disp_h))
    for y in range(0, disp_h, chip_s):  # 横線
      pg.draw.line(screen, grid_c, (0, y), (disp_w, y))

    # 移動コマンドの処理
    if cmd_move != -1:
      af_pos = bow_p + m_vec[cmd_move]
      if (0 <= af_pos.x <= map_s.x - 1) and (0 <= af_pos.y <= map_s.y - 1):
        bow_p += m_vec[cmd_move]  # 画面内に収まるならキャラ座標を実際に更新

    # 矢の更新処理
    for arrow in arrows[:]:
      arrow.updata()
      if arrow.is_off_screen(disp_h):
        arrows.remove(arrow)

    ball_spawn_timer += clock.get_time()
    if ball_spawn_timer >= 5000:
      ball_spawn_timer = 0
      new_ball = Ball(r.randint(0, int(map_s.x) - 1) * chip_s, 20, 24)
      balls.append(new_ball)

    # ボールの更新処理と描画
    for ball in balls:
      ball.updata()

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

      # hp表示
      hp_str = f"HP: {ball.hp}"
      screen.blit(font.render(hp_str, True, "BLACK"), (int(
          ball.position.x - ball.radius), int(ball.position.y - ball.radius - 10)))

    # 弓の描画、位置の更新
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
                            ball.size.x, ball.size.y)

        arrow_rect = pg.Rect(arrow.position.x, disp_h -
                             arrow.position.y, arrow.size.x, arrow.size.y)

        if arrow_rect.colliderect(ball_rect):
          # print("矢がボールに当たった")
          ball.hp -= 1
          score += 1
          arrows.remove(arrow)

          if ball.hp <= 0:
            score += ball.initial_hp
            balls.remove(ball)
          break

    # 地面描画
    for x in range(0, disp_w, int(ground_s.x)):
      screen.blit(ground_img, (x, disp_h - ground_s.y))

    # bow_hp_str = f"HP: {bow_hp}"
    # screen.blit(font.render(bow_hp_str, True, "BLACK"), (10, 50))

    score_str = f"Score: {score}"
    screen.blit(font.render(score_str, True, "BLACK"), (10, 30))

    # フレームカウンタの描画
    frame += 1
    frm_str = f'{frame:05}'
    screen.blit(font.render(frm_str, True, 'BLACK'), (10, 10))

    pg.display.update()
    clock.tick(30)

  pg.quit()
  return exit_code

if __name__ == "__main__":
  code = main()
  print(f"プログラムを「コード{code}」で終了しました。")
