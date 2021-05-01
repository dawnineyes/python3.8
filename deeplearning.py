import datetime
import os
import random
import time
import keyboard
import pyautogui
import yaml
import pyscreeze
from PIL import Image

import init_font_lib

level_lib_list = init_font_lib.init_level_lib_list()
gold_lib_list = init_font_lib.init_gold_lib_list()
draft_lib_list = init_font_lib.init_draft_lib_list()
daibi_lib_list = init_font_lib.init_daibi_lib_list()


def get_yaml_data(yaml_file):
    # 打开yaml文件
    print("***获取数据***")
    file = open(yaml_file, 'r', encoding="utf-8")
    file_data = file.read()
    file.close()
    data = yaml.load(file_data, Loader=yaml.FullLoader)
    return data


yaml_data = get_yaml_data('data.yaml')


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


def click(x, y, button='left', duration=0.1):
    dec = random.randint(-2, 2)
    # 'left', 'middle', 'right'
    x += dec
    y += dec
    # moveTo(x, y, duration=0.2)
    pyautogui.mouseDown(x, y, button=button)
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
        click_num = pic_click_all(hero_data[pic_path], min_, region=region, screenshotIm=screenshotIm)
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


def add_friend():
    id_list = yaml_data['friend_id_list']
    if len(id_list) < 1:
        return
    pic_click_one('./client/yaoqing.png', confidence=0.9)
    time.sleep(1)
    click(1183, 638)
    time.sleep(1)
    lol_hwnd = get_lol_hwnd()
    if lol_hwnd:
        x, y = lol_hwnd.box[0] + 700, lol_hwnd.box[1] + 100
    else:
        x, y = 1031, 261
    for id in id_list:
        time.sleep(1)
        click(x, y)
        time.sleep(0.5)
        slow_key_press('ctrl+a')
        time.sleep(0.5)
        slow_key_press('ctrl+x')
        time.sleep(1)
        keyboard.write(id)
        time.sleep(1)
        pic_click_one('./client/search_id.png', confidence=0.9)
    time.sleep(1)
    pic_click_one('./client/send.png', confidence=0.9)
    time.sleep(15)


def open_game(lol_hwnd=None, wait_time=60, region=None):
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
        choose_rank = yaml_data['choose_rank']
        if choose_rank:
            list_.append('./gametimeline/choose_rank.png')
        else:
            list_.append('./gametimeline/choose_match.png')
        list_.append('./gametimeline/confirm_game_mode.png')

        for pic_path in list_:
            pic_click_one(pic_path, region=region, confidence=0.7)
            time.sleep(0.7)
        time.sleep(2)
        add_friend()
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
        return self.name == game_timeline.round

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
            if game_timeline.is_rank_surrender > 0 and game_timeline.is_rank() <= game_timeline.is_rank_surrender:
                print('达到排名')
                return False
            # 选秀阶段
            if game_timeline.is_opt_hero():
                continue

            # 识别金币数量
            game_timeline.update_gold()
            # 识别等级
            game_timeline.update_level()
            # 识别回合
            update_round = game_timeline.update_round()

            if game_timeline.round > self.name:
                return True

            if game_timeline.gold >= 3:
                gg_game_(game_timeline.hero_list, game_timeline)
            game_timeline.check_list()

            if update_round is not None:
                game_timeline.click_space()
                if pic_exists('./gametimeline/choose_props.png', region=game_timeline.client_box):
                    # 正常装备 [540,700]   暗黑装备  [356,700]
                    click(game_timeline.client_box[0] + 356, game_timeline.client_box[1] + 700)
                if game_timeline.round >= 31:
                    time.sleep(1)
                    game_timeline.check_all_hero()

            # # 找5费英雄
            # pic_click_all('./role/fee5.png', region=game_timeline.find_hero_box)
            # if game_timeline.gold >= 30 and game_timeline.level >= 8 and game_timeline.find_finish():
            #     refresh_shop()
            #     pic_click_all('./role/fee5.png', region=game_timeline.find_hero_box)

            self.keep_do(game_timeline)

            if self.exists_template(game_timeline):
                self.do(game_timeline)
                return True
            game_timeline.check_level()
            # if game_timeline.is_base_init():
            game_timeline.pick_up()
            if game_timeline.round >= game_timeline.min_swipe_round:
                game_timeline.swipe_sec()

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
        self.lol_client_hwnd = get_lol_client_hwnd()
        # box 相关------------------------------------------------------------------------------------------------
        self.client_box = None
        if self.lol_client_hwnd is not None:
            self.client_box = self.lol_client_hwnd.box
        else:
            self.client_box = [445, 121, 1024, 768]
        client_x, client_y = self.client_box[0], self.client_box[1]
        # 找牌 box
        self.find_hero_box = self.add_Offset(yaml_data['game_timeline']['find_hero_box'], client_x, client_y)
        # 选秀 box
        self.opt_box = self.add_Offset(yaml_data['game_timeline']['draft_box'], client_x, client_y)
        self.rank_box = self.add_Offset(yaml_data['game_timeline']['rank_box'], client_x, client_y)
        self.fight_box = self.add_Offset(yaml_data['game_timeline']['fight_box'], client_x, client_y)
        self.watch_box = self.add_Offset(yaml_data['game_timeline']['watch_box'], client_x, client_y)

        self.gold_box = self.add_Offset(yaml_data['game_timeline']['gold_box'], client_x, client_y)
        self.level_box = self.add_Offset(yaml_data['game_timeline']['level_box'], client_x, client_y)
        self.round_box = self.add_Offset(yaml_data['game_timeline']['round_box'], client_x, client_y)
        # -------------------------------------------------------------------------------------------------------

        # 英雄信息
        self.hero_list = hero_list
        self.hero_info_list = hero_info_list
        self.hero_star_list = [0] * 20
        self.hero_max_star_list = yaml_data['game_timeline']['hero_max_star_list']

        # 英雄 数量相关
        self.add_list = add_list
        self.add_x = 0
        self.add_x_end = len(add_list)
        self.find_finish_list = [False] * (len(add_list) + 1)

        # 执行事件
        self.game_execute_list = game_execute_list

        # self.start_time = start_time
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

        # 是否开启 捡道具
        self.is_pick_up = yaml_data['game_timeline']['is_pick_up']
        self.last_pick_up_time = 0

        # 上装备  相关
        self.props_index = 0
        self.last_swipe_props_time = 0
        self.min_swipe_round = yaml_data['game_timeline']['min_swipe_round']

        # 排名达到预期 则自动投降
        self.is_rank_surrender = yaml_data['game_timeline']['is_rank_surrender']
        # 快速找牌的时间间隔
        self.fast_find_interval = yaml_data['game_timeline']['fast_find_interval']
        # 购买经验间隔
        self.upgrade_interval = yaml_data['game_timeline']['upgrade_interval']
        # 捡道具时间间隔
        self.pick_up_interval = yaml_data['game_timeline']['pick_up_interval']

        # 识别金币
        self.gold = 0
        # 识别等级
        self.level = 0
        # 识别回合 2-5   则用 数字25显示
        self.round = 0

        # 目标回合 需要达到的等级
        self.round_target_level = yaml_data['game_timeline']['round_target_level']

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

    @staticmethod
    def add_Offset(box, x, y):
        if len(box) != 4:
            raise Exception
        return [box[0] + x, box[1] + y, box[2], box[3]]

    # 购买经验 有内置cd 5秒   并且只有在金币大于34的时候才会买经验
    def upgrade_champ(self):
        if time.time() - self.last_upgrade_champ > self.upgrade_interval and self.gold >= 4:
            upgrade_champ()
            self.last_upgrade_champ = time.time()

    # 是否可以快速找牌  大于5金币才继续快速找牌
    def can_fast_find(self):
        if self.round < 33:
            m = 50
        else:
            m = 25
        if time.time() - self.last_fast_find > self.fast_find_interval and self.gold >= m:
            self.last_fast_find = time.time()
            return True
        return False

    #     一共用了多少时间
    def total_time_(self):
        time_ = time.time() - self.start_time
        print('用时' + str(int(time_ / 60.0)) + '分' + str(int(time_ % 60)) + '秒')

    def pick_up(self):
        # 3分钟 捡一次道具
        if self.is_pick_up and time.time() - self.last_pick_up_time > self.pick_up_interval:
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
    def is_opt_hero(self):
        x, y = pic_find_one('./gametimeline/draft.png', region=self.client_box)
        if x and y:
            if time.time() - self.last_draft_time > random.randint(1, 3):
                x, y = box_random_x_y(self.opt_box)
                right_click(x, y)
                self.last_draft_time = time.time()
            return True
        return False

    # 返回当前排名
    def is_rank(self):
        return 8 - len(list(pic_find_all('./gametimeline/hp0.png', confidence=0.95, region=self.rank_box)))

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
        if time.time() - self.last_print_hero_list > 10:
            print([[hero[0][hero[0].rindex('/') + 1:hero[0].rindex('.')], hero[1]] for hero in self.hero_list])
            print([star for star in self.hero_star_list[0:len(self.hero_list)]])
            self.last_print_hero_list = time.time()

    def is_base_init(self):
        return self.find_finish_list[0]

    def find_finish(self):
        for i in range(len(self.hero_list)):
            if self.hero_star_list[i] < self.hero_max_star_list[i]:
                # todo
                if self.hero_list[i][1] <= 0:
                    self.hero_list[i][1] += 1
        for i in range(len(self.hero_list)):
            if self.hero_star_list[i] < self.hero_max_star_list[i]:
                return False
        return True
        # return self.find_finish_list[self.add_x_end]

    def is_game_over(self):
        x, y = pic_click_one('./gametimeline/drop_out.png', region=self.client_box)
        if x and y:
            return True
        # lol 游戏客户端消失 游戏结束
        if get_lol_client_hwnd() is None:
            return True
        return False

    # todo 根据在场英雄血条上装备
    def swipe(self):
        # xy = random.choice(fighting_hero_xy_list)
        xy = random.choice([[518, 472], [560, 416], [519, 365], [602, 368]])
        hero_x, hero_y = xy[0] + self.client_box[0], xy[1] + self.client_box[1]
        moveTo(x=props_xy_list[self.props_index][0] + self.client_box[0],
               y=props_xy_list[self.props_index][1] + self.client_box[1])
        dragTo(hero_x, hero_y)
        self.props_index = (self.props_index + 1) % len(props_xy_list)

    def swipe_sec(self):
        if time.time() - self.last_swipe_props_time > 30:
            for i in range(6):
                self.swipe()
            self.last_swipe_props_time = time.time()

    # ----------------------------------------------------------------------------------------------
    @staticmethod
    def find_hero_health_bar(box):
        box_list = pyautogui.locateAllOnScreen('./gametimeline/hero_health_bar.png', region=box, confidence=0.75)
        result = set()
        for b in box_list:
            result.add(Pos(b[0], b[1]))
        return result

    # index大于 人口时 找空位
    def find_vacancy(self):
        for i in range(self.level):
            # 还没有该英雄  可以先上其他英雄
            if self.hero_star_list[i] <= 0:
                return i
        return None

    # 校验英雄
    def check_hero(self, box):
        result = self.find_hero_health_bar(box)
        for pos in result:
            self.click_space()
            x, y = pos.x + 25, pos.y + 53
            pyautogui.mouseDown(x, y, button='right', duration=0.1)
            pyautogui.mouseUp(button='right')
            time.sleep(0.4)
            star, index = self.find_hero_info()
            if star is None:
                pass
            else:
                # 没有info界面
                if index is None:
                    self.sell_hero(x, y)
                else:
                    # 如果 星级达到最大星级  则把 数量置为0
                    if star == self.hero_max_star_list[index]:
                        self.hero_list[index][1] = 0
                    self.hero_star_list[index] = max(self.hero_star_list[index], star)
                    if self.hero_star_list[index] == self.hero_max_star_list[index] and star < self.hero_star_list[
                        index]:
                        self.sell_hero(x, y)
                    elif index < len(fighting_hero_xy_list):
                        if self.hero_star_list[index] == star:
                            # if 人口不够
                            if index >= self.level:
                                # 找找空位
                                index = self.find_vacancy()
                            if index is not None:
                                # todo 根据英雄位置
                                dragTo(self.client_box[0] + fighting_hero_xy_list[index][0],
                                       self.client_box[1] + fighting_hero_xy_list[index][1])
        self.click_space()

    def find_hero_info(self):
        screenshotIm = pyscreeze.screenshot(region=None)
        star = self.find_star(screenshotIm)
        if star is None:
            # 没找到星级  表示没有info界面  不能判断是否卖掉英雄  只能返回true
            return None, None
        # index = 0
        for index in range(len(self.hero_info_list)):
            pos = locate(self.hero_info_list[index], screenshotIm, region=self.client_box)
            if pos is not None:
                return star, index
        try:
            screenshotIm.fp.close()
        except AttributeError:
            pass
        return star, None

    def find_star(self, screenshotIm):
        for i in range(1, 4):
            star = locate('./gametimeline/star' + str(i) + '.png', screenshotIm, region=self.client_box)
            if star is not None:
                return i
        return None

    def check_fight_hero(self):
        self.check_hero(self.fight_box)

    def check_watch_hero(self):
        self.check_hero(self.watch_box)

    def check_all_hero(self):
        self.check_hero(self.client_box)

    # ----------------------------------------------------------------------------------------------
    def check_level(self):
        for rd, target_level in self.round_target_level:
            if self.round >= rd and self.level < target_level:
                self.upgrade_champ()
                return

    # ----------------------------------------------------------------------------------------------
    # 根据 给的box, 在box中识别 lib_list中的图片 并转化未相应的字符
    # lib_list [ 图片，  找到图片后对应的字符 ]
    @staticmethod
    def ocr(box, lib_list, show=False, confidence=0.95, threshold=None):
        pic = pyscreeze.screenshot(region=box)
        if show:
            pic.show()

        if threshold:
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

        result = Game_Timeline.ocr(box, daibi_lib_list, show=False, threshold=[160, 190], confidence=0.80)
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
        return self.ocr(self.gold_box, gold_lib_list)

    def update_level(self):
        level = self.ocr_level()
        if level is not None:
            lv = self.str_to_int(level)
            if lv > self.level:
                self.level = lv
                print('level: %d.' % self.level)
        return self.level

    def ocr_level(self):
        return self.ocr(self.level_box, level_lib_list)

    # 每次到达新的回合，sleep
    def update_round(self):
        draft = self.ocr_round()
        if draft is not None:
            d = self.str_to_int(draft)
            if d > self.round:
                self.round = d
                time.sleep(2)
                print('round: %d-%d ' % (int(self.round / 10), int(self.round % 10)))
                return self.round
        return None

    def ocr_round(self):
        return self.ocr(self.round_box, draft_lib_list)

    @staticmethod
    def str_to_int(s):
        n = None
        try:
            n = int(s)
        except Exception:
            pass
        return n

    # -----------------------------------------------------------------------------------------------------------
    def click_space(self, right=False):
        click(self.client_box[0] + 140, self.client_box[1] + 460)
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
        time.sleep(0.5)
        return True
    if game_timeline.can_fast_find():
        gg_game_(game_timeline.hero_list, game_timeline)
        refresh_shop()
        gg_game_(game_timeline.hero_list, game_timeline)
        game_timeline.check_list()
    return True


def func_wait_game_over(game_timeline):
    pass


def func_1_3_normal(game_timeline):
    if len(game_timeline.find_hero_health_bar(game_timeline.client_box)) < 2:
        pic_click_one('./role/fee1.png')


def func_2_1_normal(game_timeline):
    # upgrade_champ()
    pass


def func_2_5_normal(game_timeline):
    # upgrade_champ()
    pass


def func_2_7_normal(game_timeline):
    pass


def func_3_2_normal(game_timeline):
    # upgrade_champ()
    # upgrade_champ()
    # upgrade_champ()
    pass


def func_3_3_normal(game_timeline):
    pass


def func_3_5_normal(game_timeline):
    pass


def func_3_7_normal(game_timeline):
    pass


def func_4_2_normal(game_timeline):
    # for i in range(6):
    #     upgrade_champ()
    pass


def func_5_2_normal(game_timeline):
    # for i in range(5):
    #     upgrade_champ()
    pass


run_datetime_list = []


def init_run_datetime_list():
    global run_datetime_list
    data_list = yaml_data['run_time']
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
    Game('./gametimeline/game_3_3.png', 32, func_3_2_normal, func_keep_fast_find),
    Game('./gametimeline/game_3_3.png', 33, func_3_2_normal, func_keep_fast_find),
    Game('./gametimeline/game_3_3.png', 42, func_4_2_normal, func_keep_fast_find),
    Game('./gametimeline/game_3_3.png', 52, func_5_2_normal, func_keep_fast_find),
    Game('./gametimeline/drop_out.png', 999, func_wait_game_over, func_keep_fast_find)
]

hero_list = []
add_list = []
Formation = None


def init_Formation():
    global Formation
    choose_dir = []
    for filename in os.listdir(r'./role'):
        if filename.startswith('choose'):
            choose_dir.append(filename.split('.png')[0].split('-')[1])

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


hero_num_list = yaml_data['hero_num_list']


def add_list_init():
    return yaml_data['add_list']


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
    return hero_info_list


# watch_hero_xy_list = [
#     [576, 660], [662, 660], [743, 660], [827, 660], [908, 660]
#     , [992, 660], [1075, 660], [1156, 660], [1239, 660]
# ]

# 观赛席 相对box的坐标
watch_hero_xy_list = [[124, 549], [215, 549], [301, 549], [385, 549], [466, 549], [550, 549], [633, 549], [717, 549],
                      [800, 549]]

fighting_hero_xy_list = [
    [518, 472], [560, 416], [475, 419],
    [519, 365], [602, 368], [610, 474],
    [693, 476], [650, 416], [686, 363]
]
# fighting_hero_xy_list = [[518, 472], [560, 416], [688, 366], [775, 363], [700, 472], [790, 470]]
# fighting_hero_xy_list = [[518, 472], [560, 416], [688, 366], [775, 363], [700, 472], [790, 470]]
props_xy_list = [
    [47, 549], [61, 503], [70, 460], [116, 475], [110, 465], [142, 475]
]
# ------------------------------------------------------------------------------------------------------------------
autoPaly = True
stop = False
print('start.')
time.sleep(1)

mod_ = 1
time_out = 60 * 20
num = 1

while True:
    while autoPaly:
        ckeck_time()

        activate_client()

        # 判断进入哪个分支
        #     open_game()
        time.sleep(1)
        pic_click_one('./gametimeline/OK.png', confidence=0.7)
        print('status')
        if get_lol_hwnd() is not None:
            print('open_game')
            open_game(lol_hwnd=get_lol_hwnd())
        elif get_lol_client_hwnd() is not None:
            if pic_exists('./gametimeline/In_game_logo.png', confidence=0.7):
                yaml_data = get_yaml_data('data.yaml')
                init_Formation()
                print('play_game = %d' % num, end=' ')
                print(datetime.datetime.now().strftime("%Y--%m--%d %H:%M:%S"))
                Game_Timeline(hero_list_init(), add_list_init(), normal_game_execute_list,
                              hero_info_list=hero_info_list_init()).run()
                num = num + 1
            else:
                print('loading')
        else:
            pic_click_one('./gametimeline/OK.png', confidence=0.7)

        time.sleep(3)

    time.sleep(5)
