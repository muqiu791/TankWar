import random, time, pygame, sys, HOME

from TANK import *
from BULLET import *
from EXPLODE import *
from WALL import *
from MUSIC import *

window_width = 630
window_height = 630
background_color = pygame.Color(0, 0, 0)
text_color = pygame.Color(255, 0, 0)


class main_game():
    window = None  # 创建类对象
    window_2 = None

    my_tank = None
    your_tank = None
    my_tank_life = 3
    your_tank_life = 3
    stage = 0
    num_stage = 2
    # 游戏是否结束
    is_gameover = False

    ourtank_list = []
    # 存储敌方坦克列表
    enemytank_list = []
    enemytank_count_now = 3
    enemytank_count_all = 8 * stage
    # 存储我方/敌方子弹列表：
    my_bullet_list = []


    enemy_bullet_list = []

    # 存储爆炸效果
    explode_list = []

    # 存储墙壁
    wall_list = []

    # 记录分数
    score = 0
    highest_score = 0
    # with open("Highest_Score.txt") as file:
    #     for i in file.readlines():
    #         highest_score = int(i)

    my_home = HOME.Home()

    def __init__(self):
        pass

    def start_game(self):
        pygame.display.init()
        # 后面这个函数返回一个类对象，即这个窗口
        main_game.window = pygame.display.set_mode([window_width, window_height])
        main_game.window_2 = pygame.display.set_mode([170, window_height])
        screen = pygame.display.set_mode((800, 630))

        num_player = show_start(screen)
        # 主循环
        while not main_game.is_gameover:
            # 关卡
            main_game.stage += 1
            if main_game.stage > 2:
                break

            show_switch_stage(screen, 630, 630, main_game.stage)
            time.sleep(1)  # 不然切换关卡会一闪而过

            # 重新初始化这些列表，实现关卡的内容更新

            # 不然就是两关一共只有三条命了
            main_game.my_tank_life = 3
            if num_player > 1:
                main_game.your_tank_life = 3
            else:
                main_game.your_tank_life = 0

            # 存储敌方坦克列表
            main_game.enemytank_list = []
            main_game.enemytank_count_now = 3
            main_game.enemytank_count_all = 8 * main_game.stage
            # 存储我方/敌方子弹列表：
            main_game.my_bullet_list = []
            main_game.enemy_bullet_list = []

            # 存储爆炸效果
            main_game.explode_list = []

            # 存储墙壁
            main_game.wall_list = []

            # 记录分数
            with open("Highest_Score.txt") as file:
                for i in file.readlines():
                    main_game.highest_score = int(i)

            main_game.my_home = HOME.Home()

            # 初始化我方 /敌方坦克
            self.creat_mytank(0)
            if num_player > 1:
                self.creat_mytank(1)

            for i in range(3):
                self.creat_enemytank(i)

            # 初始化墙壁
            self.creat_wall(main_game.stage)

            # 出场特效
            appearance_img = pygame.image.load("images/others/appear.png").convert_alpha()
            appearances = []
            appearances.append(appearance_img.subsurface((0, 0), (48, 48)))
            appearances.append(appearance_img.subsurface((48, 0), (48, 48)))
            appearances.append(appearance_img.subsurface((96, 0), (48, 48)))

            # 设置标题
            pygame.display.set_caption('Battle City')

            while True:
                if main_game.is_gameover is True:
                    break
                if main_game.enemytank_count_all < 1:
                    main_game.is_gameover = False
                    break

                # 防止坦克、子弹速度过快
                time.sleep(0.02)
                # 填充背景色
                main_game.window.fill(background_color)
                self.get_event(num_player)
                self._init_text(main_game.window_2)

                if main_game.my_tank and main_game.my_tank.live:
                    main_game.my_tank.display(main_game)
                else:
                    del main_game.my_tank
                    main_game.my_tank = None

                if num_player > 1:
                    if main_game.your_tank and main_game.your_tank.live:
                        main_game.your_tank.display(main_game)
                    else:
                        del main_game.your_tank
                        main_game.your_tank = None

                main_game.window.blit(main_game.my_home.image, main_game.my_home.rect)
                # 循环遍历显示这些对象
                self.blit_enemytank(appearances)
                self.blit_mybullet()
                self.blit_enemybullet()
                self.blit_explode()
                self.blit_wall()

                # 我方坦克移动
                if main_game.my_tank and main_game.my_tank.live:
                    if not main_game.my_tank.stop:
                        main_game.my_tank.move()
                        main_game.my_tank.hit_wall(main_game)
                        main_game.my_tank.hit_othertank(main_game)
                        main_game.my_tank.hit_home(main_game)
                if num_player > 1:
                    if main_game.your_tank and main_game.your_tank.live:
                        if not main_game.your_tank.stop:
                            main_game.your_tank.move()
                            main_game.your_tank.hit_wall(main_game)
                            main_game.your_tank.hit_othertank(main_game)
                            main_game.your_tank.hit_home(main_game)
                pygame.display.update()  # 更新窗口

    def end_game(self):
        with open("Highest_Score.txt",'w') as file:
            if main_game.highest_score < main_game.score:
                file.writelines(str(main_game.score))
            else:
                file.writelines(str(main_game.highest_score))
        show_end(main_game.window,main_game.is_gameover)


    def get_text_surface(self, text):
        # 初始化字体
        pygame.font.init()
        # 获取字体对象
        font = pygame.font.SysFont('kaiti', 18)
        text_surface = font.render(text, True, text_color)
        return text_surface

    def get_event(self, num_player):
        eventlist = pygame.event.get()
        for event in eventlist:
            # 鼠标关闭窗口
            if event.type == pygame.QUIT:
                exit()
            # 按下键盘
            if event.type == pygame.KEYDOWN:
                # 按esc复活
                if not main_game.my_tank and main_game.my_tank_life > 0:
                    if event.key == pygame.K_ESCAPE:
                        self.creat_mytank(0)
                if not main_game.your_tank and main_game.your_tank_life > 0:
                    if event.key == pygame.K_ESCAPE:
                        self.creat_mytank(1)

                if main_game.my_tank and main_game.my_tank.live:
                    if event.key == pygame.K_a:
                        main_game.my_tank.direction = 'L'
                        main_game.my_tank.stop = False
                    elif event.key == pygame.K_d:
                        main_game.my_tank.direction = 'R'
                        main_game.my_tank.stop = False
                    elif event.key == pygame.K_w:
                        main_game.my_tank.direction = 'U'
                        main_game.my_tank.stop = False
                    elif event.key == pygame.K_s:
                        main_game.my_tank.direction = 'D'
                        main_game.my_tank.stop = False
                    elif event.key == pygame.K_SPACE:
                        if len(self.my_bullet_list) < 10:
                            # 我方坦克发射
                            my_bullet = Bullet(main_game.my_tank)
                            self.my_bullet_list.append(my_bullet)
                            fire_music = Music('audios/fire.wav')
                            fire_music.play_music()
                if num_player > 1:
                    if main_game.your_tank and main_game.your_tank.live:
                        if event.key == pygame.K_LEFT:
                            main_game.your_tank.direction = 'L'
                            main_game.your_tank.stop = False
                        elif event.key == pygame.K_RIGHT:
                            main_game.your_tank.direction = 'R'
                            main_game.your_tank.stop = False
                        elif event.key == pygame.K_UP:
                            main_game.your_tank.direction = 'U'
                            main_game.your_tank.stop = False
                        elif event.key == pygame.K_DOWN:
                            main_game.your_tank.direction = 'D'
                            main_game.your_tank.stop = False
                        elif event.key == pygame.K_0:
                            if len(self.my_bullet_list) < 10:
                                # 我方坦克发射
                                my_bullet = Bullet(main_game.your_tank)
                                self.my_bullet_list.append(my_bullet)
                                fire_music = Music('audios/fire.wav')
                                fire_music.play_music()

            if event.type == pygame.KEYUP:
                # 不能写成  if event.key == pygame.K_a or event.key == pygame.K_d or event.key == pygame.K_w or event.key
                # == pygame.K_s:
                if event.key == pygame.K_a or event.key == pygame.K_d or event.key == pygame.K_w or event.key == pygame.K_s:
                    if main_game.my_tank and main_game.my_tank.live:
                        main_game.my_tank.stop = True
                if num_player > 1:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        if main_game.your_tank and main_game.your_tank.live:
                            main_game.your_tank.stop = True

    def creat_mytank(self, num_player):
        if num_player == 0:
            main_game.my_tank = myTank(3 + 24 * 8, 3 + 24 * 24, 1)
            main_game.ourtank_list.append(main_game.my_tank)
        elif num_player == 1:
            main_game.your_tank = myTank(3 + 24 * 16, 3 + 24 * 24, 2)
            main_game.ourtank_list.append(main_game.your_tank)
        elif num_player == 2:
            main_game.my_tank = myTank(3 + 24 * 8, 3 + 24 * 24, 1)
            main_game.your_tank = myTank(3 + 24 * 16, 3 + 24 * 24, 2)
            main_game.ourtank_list.append(main_game.my_tank)
            main_game.ourtank_list.append(main_game.your_tank)

        # 创建音乐对象并且播放
        start_music = Music('audios/start.wav')
        start_music.play_music()

    def creat_enemytank(self, x=None):
        top = 0
        left = random.randint(0, 12) * 48 + 3
        speed = 2
        enemies = enemyTank(left, top, speed, x)
        for each in main_game.enemytank_list:
            while pygame.sprite.collide_rect(enemies, each):
                enemies = enemyTank(left, top, speed, random.randint(0, 2))
        main_game.enemytank_list.append(enemies)

    def creat_wall(self, stage):
        if stage == 1:
            for x in [2, 3, 6, 7, 18, 19, 22, 23]:
                for y in [2, 3, 4, 5, 6, 7, 8, 9, 10, 17, 18, 19, 20, 21, 22, 23]:
                    brick_wall = Wall(3 + x * 24, 3 + y * 24)
                    main_game.wall_list.append(brick_wall)

            for x in [10, 11, 14, 15]:
                for y in [2, 3, 4, 5, 6, 7, 8, 11, 12, 15, 16, 17, 18, 19, 20]:
                    brick_wall = Wall(3 + x * 24, 3 + y * 24)
                    main_game.wall_list.append(brick_wall)

            for x in [4, 5, 6, 7, 18, 19, 20, 21]:
                for y in [13, 14]:
                    brick_wall = Wall(3 + x * 24, 3 + y * 24)
                    main_game.wall_list.append(brick_wall)

            for x in [12, 13]:
                for y in [16, 17]:
                    brick_wall = Wall(3 + x * 24, 3 + y * 24)
                    main_game.wall_list.append(brick_wall)

            for x, y in [(11, 23), (12, 23), (13, 23), (14, 23), (11, 24), (14, 24), (11, 25), (14, 25)]:
                brick_wall = Wall(3 + x * 24, 3 + y * 24)
                main_game.wall_list.append(brick_wall)

            for x, y in [(0, 14), (1, 14), (12, 6), (13, 6), (12, 7), (13, 7), (24, 14), (25, 14)]:
                iron_wall = Iron_wall(3 + x * 24, 3 + y * 24)
                main_game.wall_list.append(iron_wall)

        elif stage == 2:
            for y in [2]:
                for x in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 15, 16, 17, 18, 19, 20, 21, 22, 23]:
                    brick_wall = Wall(3 + x * 24, 3 + y * 24)
                    main_game.wall_list.append(brick_wall)

            for y in range(3, 19):
                for x in [2, 23]:
                    brick_wall = Wall(3 + x * 24, 3 + y * 24)
                    main_game.wall_list.append(brick_wall)

            for y in [5]:
                for x in [6, 7, 8, 9, 10, 14, 15, 16, 17, 18, 19]:
                    brick_wall = Wall(3 + x * 24, 3 + y * 24)
                    main_game.wall_list.append(brick_wall)

            for y in [6]:
                for x in [9, 10, 18, 19]:
                    brick_wall = Wall(3 + x * 24, 3 + y * 24)
                    main_game.wall_list.append(brick_wall)

            for y in [7]:
                for x in [10, 19]:
                    brick_wall = Wall(3 + x * 24, 3 + y * 24)
                    main_game.wall_list.append(brick_wall)

            for y in [10, 11]:
                for x in [12, 13]:
                    iron_wall = Iron_wall(3 + x * 24, 3 + y * 24)
                    main_game.wall_list.append(iron_wall)

            for y in [13]:
                for x in [10, 15]:
                    brick_wall = Wall(3 + x * 24, 3 + y * 24)
                    main_game.wall_list.append(brick_wall)

            for y in [14]:
                for x in [10, 11, 14, 15]:
                    brick_wall = Wall(3 + x * 24, 3 + y * 24)
                    main_game.wall_list.append(brick_wall)

            for y in [15]:
                for x in [12, 13]:
                    brick_wall = Wall(3 + x * 24, 3 + y * 24)
                    main_game.wall_list.append(brick_wall)

            for y in [19]:
                for x in range(2, 24):
                    brick_wall = Wall(3 + x * 24, 3 + y * 24)
                    main_game.wall_list.append(brick_wall)

            for x, y in [(11, 23), (12, 23), (13, 23), (14, 23), (11, 24), (14, 24), (11, 25), (14, 25)]:
                brick_wall = Wall(3 + x * 24, 3 + y * 24)
                main_game.wall_list.append(brick_wall)

            for x, y in [(0, 14), (1, 14), (24, 14), (25, 14)]:
                iron_wall = Iron_wall(3 + x * 24, 3 + y * 24)
                main_game.wall_list.append(iron_wall)

    def blit_enemytank(self, appearances):
        for enemy in main_game.enemytank_list:
            if enemy.born:
                if enemy.times > 0:
                    enemy.times -= 1
                    if enemy.times <= 10:
                        main_game.window.blit(appearances[2], (3 + enemy.x * 12 * 24, 3))
                    elif enemy.times <= 20:
                        main_game.window.blit(appearances[1], (3 + enemy.x * 12 * 24, 3))
                    elif enemy.times <= 30:
                        main_game.window.blit(appearances[0], (3 + enemy.x * 12 * 24, 3))
                    elif enemy.times <= 40:
                        main_game.window.blit(appearances[2], (3 + enemy.x * 12 * 24, 3))
                    elif enemy.times <= 50:
                        main_game.window.blit(appearances[1], (3 + enemy.x * 12 * 24, 3))
                    elif enemy.times <= 60:
                        main_game.window.blit(appearances[0], (3 + enemy.x * 12 * 24, 3))
                    elif enemy.times <= 70:
                        main_game.window.blit(appearances[2], (3 + enemy.x * 12 * 24, 3))
                    elif enemy.times <= 80:
                        main_game.window.blit(appearances[1], (3 + enemy.x * 12 * 24, 3))
                    elif enemy.times <= 90:
                        main_game.window.blit(appearances[0], (3 + enemy.x * 12 * 24, 3))
                else:
                    enemy.born = False
            elif enemy.live:
                enemy.display(main_game)
                enemy.randmove()
                enemy.hit_wall(main_game)
                enemy.enemy_hit_mytank(main_game)
                enemy.hit_othertank(main_game)
                enemy.hit_home(main_game)
                enemy_bullet = enemy.shot()
                if enemy_bullet:
                    main_game.enemy_bullet_list.append(enemy_bullet)
            else:
                main_game.enemytank_list.remove(enemy)

    def blit_mybullet(self):
        for bullet in main_game.my_bullet_list:
            if bullet.live:
                bullet.display(main_game)
                bullet.move()
                bullet.mybullet_hit_tank(main_game)
                bullet.hit_wall(main_game)
                bullet.hit_home(main_game)
                bullet.bullet_hit_bullet(main_game)
            else:
                main_game.my_bullet_list.remove(bullet)

    def blit_enemybullet(self):
        for bullet in main_game.enemy_bullet_list:
            if bullet.live:
                bullet.display(main_game)
                bullet.move()
                bullet.enemybullet_hit_mytank(main_game)
                bullet.hit_wall(main_game)
                bullet.hit_home(main_game)
            else:
                main_game.enemy_bullet_list.remove(bullet)

    def blit_explode(self):
        for explosion in main_game.explode_list:
            if explosion.live:
                explosion.display(main_game)

            else:
                main_game.explode_list.remove(explosion)

    def blit_wall(self):
        for wall in main_game.wall_list:
            if wall.live:
                wall.display(main_game)
            else:
                main_game.wall_list.remove(wall)

    def _init_text(self, screen):
        color_white = (255, 255, 255)
        self.__fix_text_tips = {
            1: {'text': '玩家1：'},
            2: {'text': 'K_w: 上'},
            3: {'text': 'K_s: 下'},
            4: {'text': 'K_a: 左'},
            5: {'text': 'K_d: 右'},
            6: {'text': 'K_SPACE: 射击'},
            8: {'text': '玩家2:'},
            9: {'text': 'K_UP: 上'},
            10: {'text': 'K_DOWN: 下'},
            11: {'text': 'K_LEFT: 左'},
            12: {'text': 'K_RIGHT: 右'},
            13: {'text': 'K_KP0: 射击'},
            15: {'text': '最高分: %s ' % self.highest_score},
            16: {'text': '当前分数: %s ' % self.score},
            17: {'text': '剩余坦克: %s' % self.enemytank_count_all},
            19: {'text': '玩家1生命: %s ' % self.my_tank_life},
            20: {'text': '玩家2生命: %s ' % self.your_tank_life},
            21: {'text': '按ESC: 复活'},
            23: {'text': '当前关卡：%s' % self.stage}
        }
        for pos, tip in self.__fix_text_tips.items():
            pygame.font.init()
            font = pygame.font.SysFont('kaiti', 18)
            tip['render'] = font.render(tip['text'], True, color_white)
            tip['rect'] = tip['render'].get_rect()
            tip['rect'].left, tip['rect'].top = window_width + 5, window_height * pos / 30
            screen.blit(tip['render'], tip['rect'])


# 显示开始界面
def show_start(window):
    pygame.font.init()
    font = pygame.font.SysFont('kaiti', 38)

    start_img = pygame.image.load("images/others/logo.png")
    content1 = font.render(u'单人模式（按1）', True, (171,130,255))
    content2 = font.render(u'双人模式（按2）', True, (171,130,255))
    content3 = font.render(u'退出（按ESC）', True, (171,130,255))
    srect = start_img.get_rect()
    srect.midtop = (800 / 2, window_height / 5)
    crect1 = content1.get_rect()
    crect1.midtop = (800 / 2, window_height / 1.8)
    crect2 = content2.get_rect()
    crect2.midtop = (800 / 2, window_height / 1.6)
    crect3 = content3.get_rect()
    crect3.midtop = (800 / 2, window_height / 1.4)
    window.blit(start_img, srect)
    window.blit(content1, crect1)
    window.blit(content2, crect2)
    window.blit(content3, crect3)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 1
                if event.key == pygame.K_2:
                    return 2
                if event.key == pygame.K_ESCAPE:
                    sys.exit()


# 关卡切换
def show_switch_stage(screen, width, height, stage):
    bg_img = pygame.image.load("images/others/background.png")
    screen.blit(bg_img, (0, 0))
    pygame.font.init()
    font = pygame.font.SysFont('kaiti', 38)
    content = font.render(u'第%d关' % stage, True, (0, 255, 0))
    rect = content.get_rect()
    rect.midtop = (width / 2, height / 2)
    screen.blit(content, rect)
    pygame.display.update()
    delay_event = pygame.constants.USEREVENT
    pygame.time.set_timer(delay_event, 1000)


# 显示结束界面
def show_end(screen, is_gameover):
    bg_img = pygame.image.load("images/others/background.png")
    screen.blit(bg_img, (0, 0))
    if not is_gameover:
        pygame.font.init()
        font = pygame.font.SysFont('kaiti', 38)
        content = font.render(u'恭喜通关！', True, (255, 0, 0))
        rect = content.get_rect()
        rect.midtop = (window_width / 2, window_height / 2)
        screen.blit(content, rect)
    else:
        fail_img = pygame.image.load("images/others/gameover.png")
        rect = fail_img.get_rect()
        rect.midtop = (window_width / 2, window_height / 2)
        screen.blit(fail_img, rect)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


if __name__ == '__main__':
    main_game().start_game()
    main_game().end_game()
    # show_end(main_game.window, main_game.is_gameover)
