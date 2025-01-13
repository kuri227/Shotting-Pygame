import random as r
import pygame as pg

def main():

  # 初期化処理
  pg.init()
  pg.display.set_caption('ぼくのかんがえたさいきょうのげーむ')
  disp_w, disp_h = 800, 600
  screen = pg.display.set_mode((disp_w, disp_h))
  clock = pg.time.Clock()
  font = pg.font.Font(None, 15)
  frame = 0
  exit_flag = False
  exit_code = '000'

  face_s = pg.Vector2(48, 48)  # サイズ
  face_r = face_s / 2          # 半径
  face_p = pg.Vector2(50, 90)  # 位置
  face_v = pg.Vector2(2, 0)   # 速度
  face_a = pg.Vector2(0, 0.2)  # 加速度
  face_img = pg.image.load(f'data/img/bow.png')
  ground_img = pg.image.load(f'data/img/map-ground.png')
  ground_s = pg.Vector2(48, 48)

  # ゲームループ
  while not exit_flag:

    # システムイベントの検出
    for event in pg.event.get():
      if event.type == pg.QUIT:
        exit_flag = True
        exit_code = '001'

    # 位置と速度の更新
    face_p += face_v
    face_v += face_a

    # 地面との衝突処理
    if face_p.y >= disp_h - ground_s.y - face_r.y:
      face_p.y = disp_h - ground_s.y - face_r.y
      face_v.y = - 0.7 * (face_v.y - face_a.y)
      if abs(face_v.y) < 3.5:
        face_v.y = 0
        face_v.x *= 0.98

    # 右端と左端との衝突
    if face_p.x + face_r.x > disp_w:
      face_p.x = disp_w - face_r.x
      face_v.x = -0.8 * face_v.x
    elif face_p.x - face_r.x < 0:
      face_p.x = face_r.x
      face_v.x = -0.8 * face_v.x

    # 地面描画
    for x in range(0, disp_w, int(ground_s.x)):
      screen.blit(ground_img, (x, disp_h - ground_s.y))

    # フレームカウンタの描画
    frame += 1
    frm_str = f'{frame:05}'
    screen.blit(font.render(frm_str, True, 'BLACK'), (10, 10))

    # 画面の更新と同期
    pg.display.update()
    clock.tick(30)

  # ゲームループ [ここまで]
  pg.quit()
  return exit_code

if __name__ == "__main__":
  code = main()
  print(f'プログラムを「コード{code}」で終了しました。')
