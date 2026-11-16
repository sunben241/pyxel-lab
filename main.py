import pyxel

WIDTH = 160
HEIGHT = 120
SPRITE = 16
SPEED = 1
FPS = 30
ANIM_FPS = 8
FRAMES_PER_TICK = max(1, FPS // ANIM_FPS)

# 圖集：image bank 0 左上角 4 欄 x 4 列，每格 16x16
# 列順序：0=上, 1=下, 2=左, 3=右
DIR_UP = 0
DIR_DOWN = 1
DIR_LEFT = 2
DIR_RIGHT = 3
ROW_OF_DIR = {DIR_UP: 0, DIR_DOWN: 1, DIR_LEFT: 2, DIR_RIGHT: 3}
COLKEY = 0

# 跳躍參數（單位：像素/幀）
JUMP_POWER = 3.2
GRAVITY = 0.35

x = (WIDTH - SPRITE) // 2
y = (HEIGHT - SPRITE) // 2
facing = DIR_DOWN
frame = 0
anim_timer = 0.0
jump_z = 0.0
jump_vz = 0.0


def update():
    global x, y, facing, frame, anim_timer, jump_z, jump_vz

    dx = 0
    dy = 0
    if pyxel.btn(pyxel.KEY_W):
        dy -= 1
    if pyxel.btn(pyxel.KEY_S):
        dy += 1
    if pyxel.btn(pyxel.KEY_A):
        dx -= 1
    if pyxel.btn(pyxel.KEY_D):
        dx += 1

    # 空白鍵跳躍（僅在地面時可起跳）
    if pyxel.btnp(pyxel.KEY_SPACE) and jump_z <= 0:
        jump_vz = JUMP_POWER

    if jump_z > 0 or jump_vz > 0:
        jump_z += jump_vz
        jump_vz -= GRAVITY
        if jump_z <= 0:
            jump_z = 0.0
            jump_vz = 0.0

    moving = dx != 0 or dy != 0

    if moving:
        # 以最後按下的方向決定朝向；同時按時優先水平
        if dx < 0:
            facing = DIR_LEFT
        elif dx > 0:
            facing = DIR_RIGHT
        elif dy < 0:
            facing = DIR_UP
        else:
            facing = DIR_DOWN

        x = min(max(x + dx * SPEED, 0), WIDTH - SPRITE)
        y = min(max(y + dy * SPEED, 0), HEIGHT - SPRITE)

        # 以幀數累積計時，約 8 幀/秒
        anim_timer += 1
        if anim_timer >= FRAMES_PER_TICK:
            anim_timer = 0
            frame = (frame + 1) % 4
    else:
        frame = 0
        anim_timer = 0


def draw():
    pyxel.cls(11)
    # 地面格線，方便看出移動
    for gx in range(0, WIDTH, 16):
        pyxel.line(gx, 0, gx, HEIGHT - 1, 5)
    for gy in range(0, HEIGHT, 16):
        pyxel.line(0, gy, WIDTH - 1, gy, 5)

    u = frame * SPRITE
    v = ROW_OF_DIR[facing] * SPRITE
    draw_y = int(y - jump_z)
    # 跳躍時在地面留下影子
    if jump_z > 0:
        pyxel.elli(x + 3, y + SPRITE - 3, SPRITE - 6, 4, 1)
    pyxel.blt(x, draw_y, 0, u, v, SPRITE, SPRITE, COLKEY)

    pyxel.text(2, 2, "WASD MOVE  SPACE JUMP", 7)


pyxel.init(WIDTH, HEIGHT, title="Panda Walk", fps=FPS)
pyxel.load("my_resource.pyxres")
pyxel.run(update, draw)
