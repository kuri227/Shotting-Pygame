import random as r
import pygame as pg

# class Playercharacter:
#   def __init__(self, init_pos, img_path):
#     self.pos = pg.Vector2(init_pos)
#     self.size = pg.Vector2(48, 48)

class Arrow:
  def __init__(self, x, y, velocity):
    self.position = pg.Vector2(x, y)
    self.velocity = velocity

  def updata(self):
    self.position += self.velocity

  def is_off_screen(self, screen_height):
    return screen_height - self.position.y < 0

def main():

  # 初期化処理
  chip_s = 48
  map_s = pg.Vector2(16, 9)

  pg.init()
  pg.display.set_caption('シューティングゲーム')
  disp_w = int(chip_s * map_s.x)
  disp_h = int(chip_s * map_s.y)
  screen = pg.display.set_mode((disp_w, disp_h))
  clock = pg.time.Clock()
  font = pg.font.Font(None, 15)
  frame = 0
  exit_flag = False
  exit_code = '000'

  # グリッド設定
  grid_c = "#bbbbbb"

  # 自キャラ移動関連のパラメータ設定
  cmd_move = -1  # 移動コマンドの管理変数
  m_vec = [
      pg.Vector2(1, 0),
      pg.Vector2(-1, 0)
  ]  # 移動コマンドに対応したXYの移動量

  # 弓の表示設定
  bow_p = pg.Vector2(2, 3)
  bow_img = pg.image.load(f'data/img/bow.png')
  bow_img = pg.transform.rotozoom(bow_img, 45, 1)
  bow_img = pg.transform.scale(bow_img, (chip_s, chip_s))
  # 弓の大きさ変更は↑から

  # 矢の表示設定
  arrows = []
  arrow_v = pg.Vector2(0, 15)
  arrow_img = pg.image.load(f"data/img/arrow.png")
  arrow_img = pg.transform.rotozoom(arrow_img, -45, 1)
  arrow_img = pg.transform.scale(arrow_img, (chip_s, chip_s))

  # ボールの表示設定
  ball_p = pg.Vector2(50, 20)  # x=50, y=90 (px)
  ball_v = pg.Vector2(5, 1)    # vx=2, vy=0 (px/frm)
  ball_a = pg.Vector2(0, 0.05)  # ax=0, ay=0.9 (px/frm^2)
  ball_s = pg.Vector2(48, 48)
  ball_r = ball_s / 2                  # ボールの半径
  ball_c = pg.Color('#ff0000')  # ボールの色

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
          arrows.append(Arrow(bow_p.x, bow_p.y + 0.5, pg.Vector2(0, 15)))

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

    # ボールの描画、位置・速度の更新
    pg.draw.circle(screen, ball_c, ball_p, ball_r.x, width=2)
    ball_p += ball_v
    ball_v += ball_a

    # 弓の描画、位置の更新
    bow_dp = pg.Vector2(bow_p.x * chip_s, disp_h - ground_s.y - chip_s)
    screen.blit(bow_img, bow_dp)

    # 矢の描画
    for arrow in arrows:
      arrow_dp = pg.Vector2(arrow.position.x * chip_s,
                            disp_h - arrow.position.y)
      screen.blit(arrow_img, arrow_dp)

    # 地面との衝突処理
    if ball_p.y >= disp_h - ground_s.y - ball_r.y:
      ball_p.y = disp_h - ground_s.y - ball_r.y
      ball_v.y = - 0.8 * (ball_v.y - ball_a.y)
      if abs(ball_v.y) < 3.5:
        ball_v.y = 0
        ball_v.x *= 0.98

    # 右端と左端との衝突処理
    if ball_p.x + ball_r.x > disp_w:
      ball_p.x = disp_w - ball_r.x
      ball_v.x = -0.8 * ball_v.x
    elif ball_p.x - ball_r.x < 0:
      ball_p.x = ball_r.x
      ball_v.x = -0.8 * ball_v.x

    # 地面描画
    for x in range(0, disp_w, int(ground_s.x)):
      screen.blit(ground_img, (x, disp_h - ground_s.y))

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
