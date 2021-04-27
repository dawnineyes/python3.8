import datetime
import os
import random
import time
import keyboard
import pyautogui
import yaml
import pyscreeze

import init_font_lib

level_lib_list = init_font_lib.init_level_lib_list()
gold_lib_list = init_font_lib.init_gold_lib_list()
draft_lib_list = init_font_lib.init_draft_lib_list()
daibi_lib_list = init_font_lib.init_daibi_lib_list()


def get_win_hwnd(title):
    try:
        w = pyautogui.getWindowsWithTitle(title)
        for i in w:
            if i.title == title:
                return i
        return None
    except Exception as e:
        return None


def get_lol_hwnd():
    return get_win_hwnd('League of Legends')


def get_lol_client_hwnd():
    return get_win_hwnd('League of Legends (TM) Client')


def get_wegame_hwnd():
    return get_win_hwnd('WeGame')


def get_start_game():
    return get_win_hwnd("腾讯云游戏")


def get_start():
    return get_win_hwnd("START")


def activate_hwnd(hwnd=None):
    if hwnd is not None:
        try:
            hwnd.restore()
            hwnd.activate()
        except Exception:
            pass


def activate_client():
    try:
        lol_hwnd = get_lol_hwnd()
        if lol_hwnd is not None:
            lol_hwnd.restore()
            lol_hwnd.activate()
        lol_client_hwnd = get_lol_client_hwnd()
        if lol_client_hwnd is not None:
            lol_client_hwnd.activate()
        time.sleep(0.5)
    except Exception as e:
        pass


def close_game():
    os.system('taskkill /IM "League of Legends.exe" /F')
    os.system('taskkill /IM LeagueClient.exe /F')
    os.system('taskkill /IM Client.exe /F')


def close_tp():
    os.system('taskkill /IM TenioDL.exe /F')
    os.system('taskkill /IM TPHelper.exe /F')
    os.system('taskkill /IM SGuard64.exe /F')
    os.system('taskkill /IM SGuardSvc64.exe /F')


def ckeck_time():
    # 在游戏中 什么都不做
    in_game = get_lol_client_hwnd() is not None
    if in_game:
        return False
    can_run = can_run_(datetime.datetime.now().time())
    if not can_run:
        close_game()
        close_tp()
        print('休息. ' + str(datetime.datetime.now().strftime("%Y--%m--%d %H:%M:%S")))


def box_center_x_y(box):
    return box[0] + int(box[2] / 2), box[1] + int(box[3] / 2)


def box_random_x_y(box):
    w_start = box[0] + int(box[2] / 5)
    w_end = box[0] + int(box[2] / 5) * 4
    h_start = box[1] + int(box[3] / 5)
    h_end = box[1] + int(box[3] / 5) * 4
    return random.randint(w_start, w_end), random.randint(h_start, h_end)


def slow_key_press(key, down_time=0.2):
    keyboard.press(key)
    time.sleep(down_time)
    keyboard.release(key)
    return True


def moveTo(x, y, duration=0.1):
    dec = random.randint(-2, 2)
    x += dec
    y += dec
    return pyautogui.moveTo(x, y, duration=duration)


def dragTo(x2, y2, duration=0.2, startx=None, starty=None):
    if startx and starty:
        moveTo(startx, starty)
    dec = random.randint(-2, 2)
    x2 += dec
    y2 += dec
    pyautogui.dragTo(x2, y2, duration=duration)


def click(x, y, button='left', duration=0.2):
    dec = random.randint(-2, 2)
    # 'left', 'middle', 'right'
    x += dec
    y += dec
    # moveTo(x, y, duration=0.2)
    pyautogui.mouseDown(x, y, button=button, duration=duration)
    time.sleep(0.1)
    pyautogui.mouseUp(button=button)


def right_click(x, y, duration=0.2):
    click(x, y, button='right', duration=duration)


def locate(image, screenshotIm, **kwargs):
    points = locateAllOnScreen(image, screenshotIm, **kwargs)
    if len(points) > 0:
        return points[0]
    return None


def locateAllOnScreen(image, screenshotIm, **kwargs):
    retVal = tuple(pyscreeze.locateAll(image, screenshotIm, **kwargs))
    return retVal


def pic_find_one(pic_path, confidence=0.95, grayscale=None, region=None):
    x, y = (None, None)
    try:
        box = pyautogui.locateOnScreen(pic_path,
                                       confidence=confidence,
                                       grayscale=grayscale,
                                       region=region)
        x, y = box_random_x_y(box)
    except Exception as e:
        return x, y
    return x, y


def pic_exists(pic_path, confidence=0.95, grayscale=None, region=None):
    x, y = pic_find_one(pic_path, confidence=confidence, grayscale=grayscale, region=region)
    if x and y:
        return True
    return False


def pic_find_all(pic_path, confidence=0.95, grayscale=None, region=None):
    return pyautogui.locateAllOnScreen(pic_path,
                                       confidence=confidence,
                                       grayscale=grayscale,
                                       region=region)


def pic_click_one(pic_path, button='left', grayscale=None, region=None, confidence=0.95):
    x, y = pic_find_one(pic_path, grayscale=grayscale, region=region, confidence=confidence)
    if x and y:
        click(x, y, button=button)
    return x, y


def pic_click_all(pic_path, max_click=99999, button='left', confidence=0.95,
                  grayscale=None, region=None, screenshotIm=None):
    if max_click <= 0:
        return 0
    if screenshotIm is None:
        box_list = pic_find_all(pic_path, confidence=confidence, grayscale=grayscale, region=region)
    else:
        box_list = locateAllOnScreen(pic_path, screenshotIm, confidence=confidence, grayscale=grayscale, region=region)
    total = 0
    for box in box_list:
        x, y = box_random_x_y(box)
        click(x, y, button=button)
        total += 1
        if total >= max_click:
            break
    return total


def find_hero(hero_list, max_click=99999, region=None):
    total = 0
    pic_path = 0
    num = 1
    screenshotIm = pyscreeze.screenshot(region=None)

    for hero_data in hero_list:
        min_ = min(hero_data[num], max_click)
        click_num = pic_click_all(hero_data[pic_path], min_, region=region, screenshotIm=screenshotIm,
                                  confidence=0.8)
        total += click_num
        hero_data[num] -= click_num
    try:
        screenshotIm.fp.close()
    except AttributeError:
        pass
    return total


# 刷新商店
def refresh_shop():
    slow_key_press('d')
    time.sleep(0.2)
    return True


# 亮表情
def show_emoji():
    slow_key_press('t')
    time.sleep(0.2)
    return True


# 提升等级
def upgrade_champ():
    slow_key_press('f')
    time.sleep(0.2)
    return True


def clear_offline_role_1(game_timeline):
    x, y = 129 + game_timeline.client_box[0], 586 + game_timeline.client_box[1]
    moveTo(x, y, duration=0.2)
    game_timeline.sell_hero(x, y)


def clear_online_role_1(game_timeline):
    x, y = 519 + game_timeline.client_box[0], 508 + game_timeline.client_box[1]
    moveTo(x, y, duration=0.2)
    game_timeline.sell_hero(x, y)


def keep_online_click():
    click(10 + random.randint(0, 10), 10 + random.randint(0, 10))


def open_game(lol_hwnd=None, wait_time=30, region=None):
    if lol_hwnd is not None:
        region = lol_hwnd.box
        pass
    # 进入云顶 寻找对局
    find = False
    if pic_exists('./gametimeline/searching_game.png', confidence=0.7, region=region):
        print('正在寻找对局')
        find = True
    else:
        list_ = [
            './gametimeline/confirm.png',
            './gametimeline/OK.png',
            './gametimeline/skip_waiting.png',
            './gametimeline/play_again.png',
            './gametimeline/Play.png',
            './gametimeline/room.png',
            './gametimeline/PvP.png',
            './gametimeline/choose_game_mode.png',
        ]
        choose_rank = get_yaml_data('data.yaml')['choose_rank']
        if choose_rank:
            list_.append('./gametimeline/choose_rank.png')
        else:
            list_.append('./gametimeline/choose_match.png')
        list_.append('./gametimeline/confirm_game_mode.png')

        for pic_path in list_:
            pic_click_one(pic_path, region=region, confidence=0.7)
            time.sleep(0.8)
        time.sleep(2)
        x, y = pic_click_one('./gametimeline/search_game.png', confidence=0.7, region=region)
        if x and y:
            find = True
    if find:
        start_time = time.time()
        while time.time() - start_time < wait_time:
            time.sleep(2)
            x, y = pic_click_one('./gametimeline/accept.png', confidence=0.7, region=region)
            if x and y:
                return True
    box = pyautogui.locateOnScreen('./gametimeline/searching_game.png', confidence=0.7)
    if box is not None:
        for i in range(3):
            click(box[0] + 202, box[1] + 14)
            time.sleep(0.5)


def open_start_game():
    start_hwnd = get_start()
    if start_hwnd is not None:
        pic_click_one('./start/my_game.png', confidence=0.7)


def gg_game_(hero_list, game_timeline, max_click=99999, region=None):
    # click(929 + game_timeline.client_box[0] + random.randint(0, 20),
    #       638 + game_timeline.client_box[1] + random.randint(-10, 10))
    # time.sleep(0.3)
    click_num = find_hero(hero_list, max_click, region=game_timeline.find_hero_box)
    return click_num


class Run_Time:
    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time

    def canRun(self, current_time):
        if self.start_time < current_time < self.end_time:
            return True
        return False

    def to_str(self):
        print(str(self.start_time) + ' ---> ' + str(self.end_time))


class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return abs(self.x - other.x) < 30 and abs(self.y - other.y) < 10

    def __lt__(self, other):
        if abs(self.x - other.x) < 30:
            return self.y + 10 < other.y
        return self.x + 30 < other.x

    def __hash__(self):
        return 0


class Game:
    # is_add = False

    def __init__(self, pic_path, name, func, keep_func):
        self.pic_path = pic_path
        self.name = name
        self.func = func
        self.keep_func = keep_func

    def exists_template(self, game_timeline):
        # if pic_exists(self.pic_path, confidence=0.95, region=region):
        return self.name == game_timeline.draft

    #     return True:继续执行   False：游戏结束
    def run(self, game_timeline):
        print('wait ' + str(self.name))
        is_ready = False
        while True:

            if stop:
                time.sleep(1)
                continue

            time.sleep(1)
            # 超过时间投降
            if game_timeline.is_time_out():
                return False
            if game_timeline.is_game_over():
                return False
            # 前四名 则直接投降
            if game_timeline.is_rank4_surrender and game_timeline.is_rank() <= 4:
                print('前四')
                return False
            # 选秀阶段
            if game_timeline.is_draft():
                continue

            # 识别金币数量
            game_timeline.update_gold()
            # 识别等级
            game_timeline.update_level()
            # 识别回合
            if game_timeline.update_draft() is not None:
                if game_timeline.draft >= 26:
                    game_timeline.check_watch_hero()

            if game_timeline.draft > self.name:
                return True

            # 找5费英雄
            pic_click_all('./role/fee5.png', region=game_timeline.find_hero_box)
            if game_timeline.gold >= 30 and game_timeline.level >= 8 and game_timeline.find_finish():
                refresh_shop()
                pic_click_all('./role/fee5.png', region=game_timeline.find_hero_box)

            self.keep_do(game_timeline)

            if self.exists_template(game_timeline):
                self.do(game_timeline)
                return True
            if game_timeline.gold >= 5:
                gg_game_(game_timeline.hero_list, game_timeline)
            game_timeline.check_list()
            # if game_timeline.is_base_init():
            game_timeline.pick_up()
            # game_timeline.swipe_sec()

    def do(self, game_timeline):
        self.func(game_timeline)
        print(self.name)

    def keep_do(self, game_timeline):
        self.keep_func(game_timeline)


class Game_Timeline:

    def __init__(self, hero_list, add_list, game_execute_list, can_check_hero=False,
                 hero_info_list=None, time_out=7200, is_pick_up=True):
        self.start_time = 0
        # 获取游戏内界面 对象
        self.lol_client_hwnd = get_start_game()
        # box 相关
        self.client_box = None
        if self.lol_client_hwnd is not None:
            self.client_box = self.lol_client_hwnd.box
        else:
            self.client_box = [445, 121, 1024, 768]
        # 找牌 box
        self.find_hero_box = [self.client_box[0], self.client_box[1] + self.client_box[3] - 120,
                              self.client_box[2], 120]

        self.hero_list = hero_list
        self.add_list = add_list
        self.game_execute_list = game_execute_list

        #         self.start_time = start_time
        self.time_out = time_out if time_out > 0 else 7200
        # self.is_add = False

        # 最后的选秀时间
        self.last_draft_time = 0
        # 最后刷新商店的时间
        self.last_upgrade_champ = 0
        # 最后快速找怪的时间
        self.last_fast_find = 0
        # 最后输出 hero_list的时间
        self.last_print_hero_list = 0

        self.is_empty = self.hero_list_is_empty()

        # 英雄 数量相关
        self.find_finish_list = []
        self.add_x = 0
        self.add_x_end = len(add_list)
        for i in range(0, len(add_list)):
            self.find_finish_list.append(False)
        self.find_finish_list.append(False)

        data = get_yaml_data('data.yaml')

        # 是否开启 捡道具
        self.is_pick_up = data['is_pick_up']
        self.last_pick_up_time = 0

        # 英雄详情信息
        self.hero_info_list = hero_info_list

        self.hero_star_list = [0] * 20

        # 上装备  相关
        self.props_index = 0
        self.last_swipe_props_time = 0
        self.can_swipe_props = True

        # 前四自动投降
        self.is_rank4_surrender = data['is_rank4_surrender']
        # 快速找牌的时间间隔
        self.fast_find_interval = data['fast_find_interval']

        # 识别金币
        self.gold = 0
        # 识别等级
        self.level = 0
        # 识别回合 2-5   则用 数字25显示
        self.draft = 0

    #         self.is_level_7 = False

    def run(self):
        self.start_time = time.time()
        for game in self.game_execute_list:
            game_running = game.run(self)
            # game_running: false 游戏结束
            if not game_running:
                self.surrender()
                break
        self.total_time_()
        return True

    # 购买经验 有内置cd 5秒   并且只有在金币大于34的时候才会买经验
    def upgrade_champ(self):
        if time.time() - self.last_upgrade_champ > 5 and self.gold >= 34:
            upgrade_champ()
            self.last_upgrade_champ = time.time()

    # 是否可以快速找牌  大于5金币才继续快速找牌
    def can_fast_find(self):
        if time.time() - self.last_fast_find > self.fast_find_interval and self.gold >= 25:
            self.last_fast_find = time.time()
            return True
        return False

    #     一共用了多少时间
    def total_time_(self):
        time_ = time.time() - self.start_time
        print('用时' + str(int(time_ / 60.0)) + '分' + str(int(time_ % 60)) + '秒')

    def pick_up(self):
        # 3分钟 捡一次道具
        if self.is_pick_up and time.time() - self.last_pick_up_time > 5:
            pic_click_one('./gametimeline/pick.png', button='right', confidence=0.7, region=self.client_box)
            pic_click_one('./gametimeline/pick2.png', button='right', confidence=0.7, region=self.client_box)
            pic_click_one('./gametimeline/pick3.png', button='right', confidence=0.7, region=self.client_box)
            pic_click_one('./gametimeline/pick4.png', button='right', confidence=0.8, region=self.client_box)
            pic_click_one('./gametimeline/pick5.png', button='right', confidence=0.8, region=self.client_box)
            self.last_pick_up_time = time.time()
            # self.swipe_props(enforce=True)
            time.sleep(1)
            return True
        return False

    # 是否选秀阶段
    def is_draft(self):
        x, y = pic_find_one('./gametimeline/draft.png', region=self.client_box)
        if x and y:
            if time.time() - self.last_draft_time > random.randint(1, 3):
                right_click(self.client_box[0] + 468 + random.randint(0, 325),
                            self.client_box[1] + 259 + random.randint(0, 210))
                self.last_draft_time = time.time()
            return True
        return False

    # 返回当前排名
    def is_rank(self):
        box_list = pic_find_all('./gametimeline/hp0.png', confidence=0.95, region=self.client_box)
        total = 0
        for box in box_list:
            total += 1
        return 8 - total

    # 投降
    def surrender(self):
        print('发起投降')
        moveTo(self.client_box[0] + 10, self.client_box[1] + 10)
        time.sleep(2)
        slow_key_press('esc')
        time.sleep(2)
        pic_click_one('./gametimeline/Initiate_surrender.png', region=self.client_box)
        time.sleep(2)
        return pic_click_one('./gametimeline/surrender.png', region=self.client_box)

    def is_time_out(self):
        return time.time() - self.start_time > self.time_out

    def hero_list_is_empty(self):
        if time.time() - self.last_print_hero_list > 10:
            print([[hero[0][hero[0].rindex('/') + 1:hero[0].rindex('.')], hero[1]] for hero in self.hero_list])
            self.last_print_hero_list = time.time()
        for hero_data in self.hero_list:
            if hero_data[1] > 0:
                return False
        return True

    def update_is_empty(self):
        self.is_empty = self.hero_list_is_empty()
        return self.is_empty

    def hero_list_add(self):
        num = 1
        for i in range(len(self.hero_list)):
            self.hero_list[i][num] += self.add_list[self.add_x][i]
        return True

    # ------------------------------------------------------------------------------------------------------------------
    # 校验英雄数量
    def check_list(self):
        if not self.find_finish_list[self.add_x]:
            self.find_finish_list[self.add_x] = self.update_is_empty()
            if self.find_finish_list[self.add_x]:
                print('finish.')
                if self.add_x < self.add_x_end:
                    self.hero_list_add()
                    print('add. ' + str(self.add_x))
                    self.add_x = self.add_x + 1

    def is_base_init(self):
        return self.find_finish_list[0]

    def find_finish(self):
        for i in range(len(self.hero_list)):
            if self.hero_star_list[i] < 2:
                # todo
                if self.hero_list[i][1] <= 0:
                    self.hero_list[i][1] += 1
                return False
        return True
        # return self.find_finish_list[self.add_x_end]

    def is_game_over(self):
        x, y = pic_click_one('./gametimeline/drop_out.png', region=self.client_box, confidence=0.8)
        if x and y:
            return True
        # lol 游戏客户端消失 游戏结束
        # if get_lol_client_hwnd() is None:
        #     return True
        return False

    def swipe(self):
        xy = random.choice(fighting_hero_xy_list)
        hero_x, hero_y = xy[0] + self.client_box[0], xy[1] + self.client_box[1]
        moveTo(x=props_xy_list[self.props_index][0] + self.client_box[0],
               y=props_xy_list[self.props_index][1] + self.client_box[1])
        dragTo(hero_x, hero_y)
        self.props_index = (self.props_index + 1) % len(props_xy_list)

    def swipe_sec(self):
        if time.time() - self.last_swipe_props_time > 35:
            for i in range(6):
                self.swipe()
            self.last_swipe_props_time = time.time()

    # ----------------------------------------------------------------------------------------------
    # 校验英雄
    def check_hero(self, box):
        box_list = pyautogui.locateAllOnScreen('./gametimeline/hero_health_bar.png', region=box, confidence=0.75)
        result = set()
        for b in box_list:
            result.add(Pos(b[0], b[1]))
        for pos in result:
            self.click_space()
            x, y = pos.x + 25, pos.y + 50
            pyautogui.mouseDown(x, y, button='right', duration=0.2)
            pyautogui.mouseUp(button='right')
            time.sleep(0.5)
            star_index = self.find_hero_info()
            if star_index is None:
                self.sell_hero(x, y)
            else:
                # 没有info界面
                if star_index[0] == 0:
                    pass
                else:
                    star = star_index[0]
                    index = star_index[1]
                    if star < self.hero_star_list[index]:
                        self.sell_hero(x, y)
                    self.hero_star_list[index] = max(self.hero_star_list[index], star)
                    if index < len(fighting_hero_xy_list):
                        dragTo(self.client_box[0] + fighting_hero_xy_list[index][0],
                               self.client_box[1] + fighting_hero_xy_list[index][1])
        self.click_space()

    def find_hero_info(self):
        screenshotIm = pyscreeze.screenshot(region=None)
        star = self.find_star(screenshotIm)
        if star is None:
            # 没找到星级  表示没有info界面  不能判断是否卖掉英雄  只能返回true
            return [0, -1]
        index = 0
        for hero_info in self.hero_info_list:
            pos = locate(hero_info, screenshotIm, region=self.client_box)
            if pos is not None:
                return [star, index]
            index += 1
        try:
            screenshotIm.fp.close()
        except AttributeError:
            pass
        return None

    def find_star(self, screenshotIm):
        for i in range(1, 4):
            star = locate('./gametimeline/star' + str(i) + '.png', screenshotIm, region=self.client_box)
            if star is not None:
                return i
        return None

    def find_health_bar(self):
        box_list = list(pyautogui.locateAllOnScreen('./gametimeline/hero_health_bar.png',
                                                    region=self.client_box, confidence=0.8))
        result = set()
        for box in box_list:
            result.add(Pos(box[0], box[1]))
        return result

    def check_watch_hero(self):
        fight_box = [self.client_box[0] + 28, self.client_box[1] + 158, 890, 305]
        watch_box = [self.client_box[0] + 28, self.client_box[1] + 158 + 305, 890, 150]
        self.check_hero(self.client_box)

    # ----------------------------------------------------------------------------------------------
    # 根据 给的box, 在box中识别 lib_list中的图片 并转化未相应的字符
    # lib_list [ 图片，  找到图片后对应的字符 ]
    @staticmethod
    def ocr(box, lib_list, show=False, confidence=0.95, convert_2_=False, threshold=[160, 190]):
        pic = pyscreeze.screenshot(region=box)
        if show:
            pic.show()

        if convert_2_:
            pic = Game_Timeline.convert_2(pic, threshold=threshold)

        list = []
        for path_and_name in lib_list:
            path = path_and_name[0]
            name = path_and_name[1]
            points = tuple(pyscreeze.locateAll(path, pic, confidence=confidence))
            if len(points):
                for point in points:
                    # 根据x坐标排序
                    list.append((point[0], name))
        # x轴小的 排前面
        list.sort()
        s = ''
        for n in list:
            s += str(n[1])
        try:
            pic.fp.close()
        except Exception:
            pass
        if s == '':
            return None
        return s

    @staticmethod
    def convert_2(img, threshold=[0, 255]):
        img = img.convert('L')
        min_ = threshold[0]
        max_ = threshold[1]
        table = []
        for i in range(256):
            if min_ <= i <= max_:
                table.append(1)
            else:
                table.append(0)
        # convert to binary image by the table
        bim = img.point(table, '1')
        return bim

    @staticmethod
    def ocr_daibi():
        box = pyautogui.locateOnScreen('./client/daibi.png', confidence=0.95)
        if box is None:
            return None
        box = [box[0], box[1], 68, 68]

        result = Game_Timeline.ocr(box, daibi_lib_list, show=False, convert_2_=True, threshold=[160, 190],
                                   confidence=0.80)
        return Game_Timeline.str_to_int(result)

    @staticmethod
    def box_pic(box):
        pic = pyscreeze.screenshot(region=box)
        pic.show()
        pic.save('./daibi.png')
        try:
            pic.fp.close()
        except Exception:
            pass

    # 识别 等级，回合、金币--------------------------------------------------------------------------------------
    def update_gold(self):
        gold = self.ocr_gold()
        if gold is not None:
            g = self.str_to_int(gold)
            if g != self.gold:
                self.gold = g
                print('gold: %d.' % self.gold)
        return self.gold

    def ocr_gold(self):
        gold_box = [566, 584, 46, 26]
        gold_box[0] += self.client_box[0]
        gold_box[1] += self.client_box[1]
        return self.ocr(gold_box, gold_lib_list)

    def update_level(self):
        level = self.ocr_level()
        if level is not None:
            lv = self.str_to_int(level)
            if lv > self.level:
                self.level = lv
                print('level: %d.' % self.level)
                # 到达等级7  清空watch
                # if self.level >= 7:
                #     for pos in watch_hero_xy_list:
                #         self.sell_hero(self.client_box[0] + pos[0], self.client_box[1] + pos[1])
                #         time.sleep(0.3)
        return self.level

    def ocr_level(self):
        level_box = [177, 584, 35, 26]
        level_box[0] += self.client_box[0]
        level_box[1] += self.client_box[1]
        return self.ocr(level_box, level_lib_list)

    # 每次到达新的回合，sleep 1秒
    def update_draft(self):
        draft = self.ocr_draft()
        if draft is not None:
            d = self.str_to_int(draft)
            if d > self.draft:
                self.draft = d
                time.sleep(2)
                print('draft: %d-%d ' % (int(self.draft / 10), int(self.draft % 10)))
                # print('新回合', end=' ')
                # self.right_click_watch()
                return self.draft
        return None

    def ocr_draft(self):
        draft_box = [480, 0, 160, 26]
        draft_box[0] += self.client_box[0]
        draft_box[1] += self.client_box[1]
        return self.ocr(draft_box, draft_lib_list)

    @staticmethod
    def str_to_int(s):
        n = None
        try:
            n = int(s)
        except Exception:
            pass
        return n

    # -----------------------------------------------------------------------------------------------------------
    # 校验观赛席
    def exists_hero_on_watch(self):
        watch_box = [self.client_box[0] + 55, self.client_box[1] + 474, 831, 143]
        # 用血条查找英雄位置
        box_list = pyautogui.locateAllOnScreen('./gametimeline/hero_health_bar.png', region=watch_box, confidence=0.8)
        x_list = []
        for b in box_list:
            x = b[0] + int(b[2] / 2) - self.client_box[0]
            x_list.append(x)
        x_list.sort()
        # print(x_list)
        visit_list = [False for i in range(9)]
        visit_index_list = []
        max_xy = 0
        for x in x_list:
            for j in range(9):
                if abs(x - watch_hero_xy_list[j][0]) < 40:
                    max_xy = max(abs(x - watch_hero_xy_list[j][0]), max_xy)
                    if not visit_list[j]:
                        visit_index_list.append(j)
                    visit_list[j] = True
        print('max_x: %d. ' % max_xy, end=' ')
        visit_index_list.sort()
        print(visit_index_list)

        return visit_index_list

    def right_click_watch(self):
        visit_index_list = self.exists_hero_on_watch()
        for index in visit_index_list:
            x = watch_hero_xy_list[index][0] + self.client_box[0]
            y = watch_hero_xy_list[index][1] + self.client_box[1]
            right_click(x, y)
            time.sleep(0.5)
            self.click_space()

    def click_space(self, right=False):
        click(self.client_box[0] + 314, self.client_box[1] + 422)
        if right:
            click(self.client_box[0] + 140, self.client_box[1] + 460, button='right')

    # -----------------------------------------------------------------------------------------------------------
    @staticmethod
    def sell_hero(x, y):
        pyautogui.mouseDown(x, y, button='left', duration=0.2)
        slow_key_press('e')
        time.sleep(0.1)
        pyautogui.mouseUp(button='left')


def can_run_(current_time):
    for run_time in run_datetime_list:
        if run_time.canRun(current_time):
            return True
    return False


def change_game_status():
    global autoPaly
    autoPaly = not autoPaly
    print('change_game_status.  ' + ('running' if autoPaly else 'stop'))
    return autoPaly


def stop_game():
    global stop
    stop = not stop
    print('%s.' % ['running', 'stop'][stop])
    return stop


keyboard.add_hotkey('F12', change_game_status)
keyboard.add_hotkey('F11', stop_game)


def func_keep_find(game_timeline):
    if game_timeline.find_finish():
        time.sleep(0.5)
        return True


def func_keep_fast_find(game_timeline):
    if game_timeline.find_finish():
        game_timeline.upgrade_champ()
        time.sleep(0.5)
        return True
    if game_timeline.can_fast_find():
        gg_game_(game_timeline.hero_list, game_timeline)
        refresh_shop()
        gg_game_(game_timeline.hero_list, game_timeline)
        game_timeline.check_list()
    return True


def func_wait_game_over(game_timeline):
    print('游戏结束了')
    pic_click_one("gametimeline/drop_out.png")


def func_1_3_normal(game_timeline):
    pic_click_one('./role/fee1.png')


def func_2_1_normal(game_timeline):
    # if len(game_timeline.find_health_bar()) < 3:
    # pic_click_one('./role/fee1.png')
    pass


def func_2_5_normal(game_timeline):
    time.sleep(2)
    # clear_offline_role_1(game_timeline)


def func_2_7_normal(game_timeline):
    time.sleep(2)
    # clear_online_role_1(game_timeline)
    upgrade_champ()
    # gg_game_(game_timeline.hero_list, game_timeline)
    # refresh_shop()
    # gg_game_(game_timeline.hero_list, game_timeline)


def func_3_3_normal(game_timeline):
    time.sleep(2)
    upgrade_champ()
    upgrade_champ()
    # upgrade_champ()
    # upgrade_champ()
    # gg_game_(game_timeline.hero_list, game_timeline)
    # refresh_shop()
    # gg_game_(game_timeline.hero_list, game_timeline)
    # time.sleep(70)
    pass


def func_3_5_normal(game_timeline):
    time.sleep(2)
    upgrade_champ()
    # clear_offline_role_1(game_timeline)
    pass


def func_3_7_normal(game_timeline):
    time.sleep(1)
    time.sleep(0.5)


def get_yaml_data(yaml_file):
    # 打开yaml文件
    print("***获取数据***")
    file = open(yaml_file, 'r', encoding="utf-8")
    file_data = file.read()
    file.close()
    data = yaml.load(file_data, Loader=yaml.FullLoader)
    return data


run_datetime_list = []


def init_run_datetime_list():
    global run_datetime_list
    data_list = get_yaml_data('data.yaml')['run_time']
    for data in data_list:
        start_h, start_m = data['start_time'][0], data['start_time'][1]
        end_h, end_m = data['end_time'][0], data['end_time'][1]

        run_datetime_list.append(Run_Time(datetime.time(start_h, start_m), datetime.time(end_h, end_m)))


init_run_datetime_list()
rest_list = [
    './gametimeline/Home.png',
    './gametimeline/TFT.png',
    './gametimeline/Champions_League.png',
    './gametimeline/career .png',
    './gametimeline/Collection.png',
    './gametimeline/trophy.png'
]

normal_game_execute_list = [
    Game('./gametimeline/game_1_3.png', 13, func_1_3_normal, func_keep_find),
    Game('./gametimeline/game_2_1.png', 21, func_2_1_normal, func_keep_find),
    Game('./gametimeline/game_2_5.png', 25, func_2_5_normal, func_keep_find),
    Game('./gametimeline/game_2_7.png', 27, func_2_7_normal, func_keep_find),
    Game('./gametimeline/game_3_3.png', 33, func_3_3_normal, func_keep_find),
    Game('./gametimeline/game_3_5.png', 35, func_3_5_normal, func_keep_find),
    Game('./gametimeline/drop_out.png', 999, func_wait_game_over, func_keep_fast_find)
]

hero_list = []
add_list = []
Formation = None

choose_dir = []
for filename in os.listdir(r'./role'):
    if filename.startswith('choose'):
        choose_dir.append(filename.split('.png')[0].split('-')[1])


def init_Formation():
    global Formation
    interim = [''] * 10
    formation_x = random.choice(choose_dir)
    print('choose-' + formation_x)
    choose_role_num = 0
    for filename in os.listdir(r'./role/choose-' + formation_x):
        name_and_index = filename.split('.png')[0].split('-')
        name = name_and_index[0]
        index = int(name_and_index[1])
        interim[index] = name
        choose_role_num += 1
    fm = []
    for i in range(choose_role_num):
        fm.append(interim[i])
    Formation = fm


hero_num_list = [3, 3, 3, 3, 3, 3]


def add_list_init():
    return [[0, 0, 0, 0, 0, 0]]


def hero_list_init():
    hero_list = []
    i = 0
    for hero_name in Formation:
        hero_list.append(['./role/' + hero_name + '.png', hero_num_list[i]])
        i += 1
    return hero_list


def hero_info_list_init():
    hero_info_list = []
    for hero_name in Formation:
        hero_info_list.append('./role/roleinfo/' + hero_name + '.png')
    hero_info_list.append('./role/roleinfo/fee5.png')
    hero_info_list.append('./role/roleinfo/fee14.png')
    return hero_info_list


# watch_hero_xy_list = [
#     [576, 660], [662, 660], [743, 660], [827, 660], [908, 660]
#     , [992, 660], [1075, 660], [1156, 660], [1239, 660]
# ]

# 观赛席 相对box的坐标
watch_hero_xy_list = [[124, 549], [215, 549], [301, 549], [385, 549], [466, 549], [550, 549], [633, 549], [717, 549],
                      [800, 549]]

fighting_hero_xy_list = [[518, 472], [475, 419], [519, 365], [610, 474], [560, 416], [602, 368]]
props_xy_list = [
    [44, 567], [50, 544], [50, 529], [80, 507], [65, 475],
    # [120, 506],   可能会点到英雄
    [104, 475],
    [71, 460], [111, 460], [142, 475]
]

# ------------------------------------------------------------------------------------------------------------------
autoPaly = True
stop = False
print('start.')
time.sleep(1)

mod_ = 1
time_out = 60 * 11
num = 1

while True:
    while autoPaly:

        # 判断进入哪个分支
        #     open_game()
        time.sleep(1)
        # pic_click_one('./gametimeline/OK.png', confidence=0.7)
        print('status')
        start_game_hwnd = get_start_game()
        if start_game_hwnd is None:
            pass
            # open_start_game()
        activate_hwnd(start_game_hwnd)

        if pic_exists('./gametimeline/mark_waiting_game.png', confidence=0.7):
            print('open_game')
            open_game(lol_hwnd=get_lol_hwnd())
        elif pic_exists('./gametimeline/In_game_logo.png', confidence=0.7):
            init_Formation()
            print('play_game = %d' % num, end=' ')
            print(datetime.datetime.now().strftime("%Y--%m--%d %H:%M:%S"))
            Game_Timeline(hero_list_init(), add_list_init(), normal_game_execute_list,
                          hero_info_list=hero_info_list_init()).run()
            num = num + 1
        else:
            pic_click_one('./gametimeline/OK.png', confidence=0.7)
            print('loading')

        time.sleep(2)

    time.sleep(5)
