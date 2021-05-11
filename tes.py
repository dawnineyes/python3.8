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


def log_print(s:str,end=None):
    print(s,end=end)


def get_yaml_data(yaml_file):
    # 打开yaml文件
    log_print("***获取数据***")
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
        # close_tp()
        log_print('休息. ' + str(datetime.datetime.now().strftime("%Y--%m--%d %H:%M:%S")))


def box_center_x_y(box):
    return box[0] + int(box[2] / 2), box[1] + int(box[3] / 2)


def box_random_x_y(box):
    w_start = box[0] + int(box[2] / 5)
    w_end = box[0] + int(box[2] / 5) * 4
    h_start = box[1] + int(box[3] / 5)
    h_end = box[1] + int(box[3] / 5) * 4
    return random.randint(w_start, w_end), random.randint(h_start, h_end)


def slow_key_press(key, down_time=0.1):
    keyboard.press(key)
    time.sleep(down_time)
    keyboard.release(key)
    return True


def moveTo(x, y, duration=0.1):
    dec = random.randint(-2, 2)
    x += dec
    y += dec
    # pyautogui.easeInQuad              start slow, end fast
    # pyautogui.easeOutQuad             start fast, end slow
    return pyautogui.moveTo(x, y, duration, pyautogui.easeOutQuad)


def curve_moveTo(x, y, end_x, end_y):
    for i in range(20):
        step_x, step_y = end_x - x, end_y - y
        x, y = x + int(step_x / 10) + random.randint(-50, 50), y + int(step_y / 10) + random.randint(-50, 50)
        pyautogui.moveTo(x, y)
    pyautogui.moveTo(end_x, end_y)


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
    moveTo(x, y, duration=0.1)
    pyautogui.mouseDown(x, y, button=button,duration=duration)
    # time.sleep(0.1)
    pyautogui.mouseUp(button=button)


def right_click(x, y, duration=0.1):
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
    moveTo(x, y, duration=0.1)
    game_timeline.sell_hero(x, y)


def clear_online_role_1(game_timeline):
    x, y = 519 + game_timeline.client_box[0], 508 + game_timeline.client_box[1]
    moveTo(x, y, duration=0.1)
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
        log_print('正在寻找对局')
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


class Run_Time:
    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time

    def canRun(self, current_time):
        if self.start_time < current_time < self.end_time:
            return True
        return False

    def to_str(self):
        log_print(str(self.start_time) + ' ---> ' + str(self.end_time))


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


class Hero_pos:
    def __init__(self, index: int, star: int, pos: Pos, is_tibu: bool):
        self.index = index
        self.star = star
        self.pos = pos
        self.is_tibu = is_tibu
        # self.on_fight = on_fight

    def priority(self, other):
        if other is None:
            return True
        return self.priority_num() > other.priority_num()

    def pri_and_eq(self, other):
        if other is None:
            return True
        return self.priority_num() >= other.priority_num()

    def not_priority(self, other):
        return self.priority_num() < other.priority_num()

    def priority_num(self):
        if self.index is None:
            return -1
        result = 0
        if not self.is_tibu:
            result += 10000
        result += self.star * 100
        # if self.on_fight:
        #     result += 1
        return result


class Props_Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return abs(self.x - other.x) < 30 and abs(self.y - other.y) < 30

    def __lt__(self, other):
        if abs(self.x - other.x) < 30:
            return self.y + 30 < other.y
        return self.x + 30 < other.x

    def __str__(self):
        return str((self.x, self.y))

    def __hash__(self):
        return 0


class Props:
    def __init__(self, props_param_list: list, pos):
        self.key = self.get_key(props_param_list)
        self.pos = pos

    def __eq__(self, other):
        return self.key == other.key

    def __hash__(self):
        return self.key

    # 根据单个装备的参数     获取相应的key
    @staticmethod
    def get_key(props_param_list):
        props_param_list.sort()
        result = ''
        for param in props_param_list:
            result = result + param + '-'
        result = result[:-1]
        return result

    # 拆解配置文件 装备信息的 + 表示多个小件    -表示同一个装备的多个属性
    @staticmethod
    def split_and_get_key(key: str):
        prop_list = key.split('+')
        key_list = []
        for prop_param in prop_list:
            p_l = prop_param.split('-')
            p_key = Props.get_key(p_l)
            key_list.append(p_key)
        key_list.sort()
        result = ''
        for key in key_list:
            result = result + key + '+'
        result = result[:-1]
        return result


class Props_Info:

    def __init__(self, hero_dic_list, game_timeline):
        self.game_timeline = game_timeline
        self.hero_need_props_info = {}
        self.props_type_list = [None] * len(self.game_timeline.hero_dic_list)
        self.props_dic = {}
        for index in range(len(hero_dic_list)):
            hero_dic = hero_dic_list[index]
            for props_name in hero_dic['props']:
                key = Props.split_and_get_key(props_name)
                # log_print(key)
                if key not in self.hero_need_props_info.keys():
                    self.hero_need_props_info[key] = []
                self.hero_need_props_info[key].append(index)

    def init(self):
        self.props_type_list = [None] * len(self.game_timeline.hero_dic_list)
        self.props_dic = {}

    @staticmethod
    def restore(arr):
        for props_pos_list, props_pos in arr:
            props_pos_list.append(props_pos)

    # 找不到 return []   找到了 return [Props_pos,...]  返回需要的装备的pos list
    def have_props(self, key):
        keys = self.props_dic.keys()
        arr = []
        result = []
        # 先找成型装备
        if key in keys:
            props_pos_list = self.props_dic[key]
            if len(props_pos_list) > 0:
                result.append(props_pos_list.pop())
                return result
        # 找不到成型装备 则 看看散件能不能合成
        param_list = self.split_props_name(key)
        for props_name in param_list:
            if props_name not in keys:
                return []
            else:
                props_pos_list = self.props_dic[props_name]
                if len(props_pos_list) <= 0:
                    self.restore(arr)
                    return []
                else:
                    arr.append([props_pos_list, props_pos_list.pop()])
        for props_pos_list, props_pos in arr:
            result.append(props_pos)
        return result

    def have_props_to_hero(self):
        for props_key, hero_index_list in self.hero_need_props_info.items():
            if len(hero_index_list) > 0:
                props_pos_list = self.have_props(props_key)
                if len(props_pos_list) > 0:
                    # log_print('have_props_to_hero ' + str(hero_index_list))
                    # todo 不要随机
                    hero_index = random.choice(hero_index_list)
                    hero_pos = self.game_timeline.fight_hero_pos_list[hero_index]
                    if hero_pos is not None and not hero_pos.is_tibu and hero_pos.index == hero_index:
                        for props_pos in props_pos_list:
                            pyautogui.moveTo(props_pos.x, props_pos.y)
                            dragTo(hero_pos.pos.x, hero_pos.pos.y)
                            time.sleep(0.1)
                        # log_print('装备 ' + props_key + ' dragTo ' + str(hero_index))
                        hero_index_list.remove(hero_index)

    @staticmethod
    def split_props_name(name: str):
        return name.split('+')


class Game:
    # is_add = False

    def __init__(self, pic_path, name, func, keep_func):
        self.pic_path = pic_path
        self.name = name
        self.func = func
        self.keep_func = keep_func

    def exists_template(self, game_timeline):
        return self.name == game_timeline.round

    #     return True:继续执行   False：游戏结束
    def run(self, game_timeline):
        log_print('wait ' + str(self.name))
        is_ready = False
        while True:
            time.sleep(1)
            s_time = time.time()
            if stop:
                continue

            # 超过时间投降
            if game_timeline.is_time_out():
                return False
            if game_timeline.is_game_over():
                return False
            # 前四名 则直接投降
            if game_timeline.is_rank_surrender > 0 and game_timeline.is_rank() <= game_timeline.is_rank_surrender:
                log_print('达到排名')
                return False
            # 选秀阶段
            if game_timeline.is_opt_hero():
                continue
            # log_print('识别选秀用时: %s' %(time.time()-s_time))
            # s_time = time.time()
            # 识别回合、等级、金币
            update_round, update_level, update_gold = game_timeline.update_round_level_gold()
            # log_print('识别回合、等级、金币用时: %s' %(time.time()-s_time))
            # s_time = time.time()

            if game_timeline.round > self.name:
                return True

            if game_timeline.gold >= 3:
                if search_hero(game_timeline) > 0:
                    time.sleep(1)
            if update_round is not None:
                game_timeline.click_space()
                if pic_exists('./gametimeline/choose_props.png', region=game_timeline.client_box):
                    # 正常装备 [540,700]   暗黑装备  [356,700]
                    rx, ry = random.choice([[540, 700], [356, 700]])
                    click(game_timeline.client_box[0] + rx, game_timeline.client_box[1] + ry)
                if game_timeline.round >= game_timeline.min_sell_round:
                    game_timeline.check_all_hero()
                else:
                    # 如果可上场英雄 达到人口数，那就提前删英雄
                    if game_timeline.check_all_hero(sell=False) >= game_timeline.level:
                        game_timeline.min_sell_round = game_timeline.round
                # log_print('校验英雄用时: %s' %(time.time()-s_time))
                # s_time = time.time()
            else:
                pass

            self.keep_do(game_timeline)

            if self.exists_template(game_timeline):
                self.do(game_timeline)
                return True
            game_timeline.check_level()
            game_timeline.pick_up()
            # log_print('用时: %s' % (time.time() - s_time))

    def do(self, game_timeline):
        self.func(game_timeline)
        log_print(self.name)

    def keep_do(self, game_timeline):
        self.keep_func(game_timeline)


class Game_Timeline:

    def __init__(self, game_execute_list, time_out=7200):
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
        self.opt_box = self.add_Offset(yaml_data['game_timeline']['opt_box'], client_x, client_y)
        self.rank_box = self.add_Offset(yaml_data['game_timeline']['rank_box'], client_x, client_y)
        self.fight_box = self.add_Offset(yaml_data['game_timeline']['fight_box'], client_x, client_y)
        self.watch_box = self.add_Offset(yaml_data['game_timeline']['watch_box'], client_x, client_y)
        self.props_box = self.add_Offset(yaml_data['game_timeline']['props_box'], client_x, client_y)

        self.gold_box = self.add_Offset(yaml_data['game_timeline']['gold_box'], client_x, client_y)
        self.level_box = self.add_Offset(yaml_data['game_timeline']['level_box'], client_x, client_y)
        self.round_box = self.add_Offset(yaml_data['game_timeline']['round_box'], client_x, client_y)
        # -------------------------------------------------------------------------------------------------------

        # 英雄信息
        self.hero_dic_list = init_hero_dic_list()
        self.fight_hero_pos_list = [None] * len(self.hero_dic_list)
        # 最小删除英雄回合
        self.min_sell_round = yaml_data['game_timeline']['min_sell_round']

        # 执行事件
        self.game_execute_list = game_execute_list

        self.time_out = time_out

        # 最后的选秀时间
        self.last_draft_time = 0
        # 最后刷新商店的时间
        self.last_upgrade_champ = 0
        # 最后快速找怪的时间
        self.last_fast_find = 0
        # 最后输出 hero_list的时间
        self.last_print_hero_list = 0

        # 是否开启 捡道具
        self.is_pick_up = yaml_data['game_timeline']['is_pick_up']
        self.last_pick_up_time = 0

        # 上装备  相关
        self.props_index = 0
        self.last_swipe_props_time = 0
        self.min_swipe_round = yaml_data['game_timeline']['min_swipe_round']
        self.props_info = Props_Info(self.hero_dic_list, self)

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
        self.level = 2
        # 识别回合 2-5   则用 数字25显示
        self.round = 0

        # 目标回合 需要达到的等级
        self.round_target_level_list = yaml_data['game_timeline']['round_target_level_list']
        # 购买经验的 金币阈值
        self.upgrade_threshold = yaml_data['game_timeline']['upgrade_threshold']
        self.check_level_threshold = yaml_data['game_timeline']['check_level_threshold']

        self.can_fast_find_round = yaml_data['game_timeline']['can_fast_find_round']

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
        if time.time() - self.last_upgrade_champ > self.upgrade_interval:
            upgrade_champ()
            self.last_upgrade_champ = time.time()

    # 是否可以快速找牌  大于5金币才继续快速找牌
    def can_fast_find(self):
        if self.round < self.can_fast_find_round:
            m = 55
        else:
            m = self.upgrade_threshold
        if time.time() - self.last_fast_find > self.fast_find_interval and self.gold >= m:
            self.last_fast_find = time.time()
            return True
        return False

    #     一共用了多少时间
    def total_time_(self):
        time_ = time.time() - self.start_time
        log_print('用时' + str(int(time_ / 60.0)) + '分' + str(int(time_ % 60)) + '秒')

    def pick_up(self):
        # 3分钟 捡一次道具
        if self.is_pick_up and time.time() - self.last_pick_up_time > self.pick_up_interval:
            pic_click_one('./gametimeline/pick.png', button='right', confidence=0.7, region=self.client_box)
            # pic_click_one('./gametimeline/pick2.png', button='right', confidence=0.7, region=self.client_box)
            pic_click_one('./gametimeline/pick3.png', button='right', confidence=0.7, region=self.client_box)
            # pic_click_one('./gametimeline/pick4.png', button='right', confidence=0.8, region=self.client_box)
            pic_click_one('./gametimeline/pick5.png', button='right', confidence=0.8, region=self.client_box)
            self.last_pick_up_time = time.time()
            return True
        return False

    # 是否选秀阶段
    def is_opt_hero(self):
        # todo 可以优化 到配置文件里面
        box = [self.client_box[0], self.client_box[1], self.client_box[2], 60]
        x, y = pic_find_one('./gametimeline/draft.png', region=box)
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
        log_print('发起投降')
        moveTo(self.client_box[0] + 10, self.client_box[1] + 10)
        time.sleep(2)
        slow_key_press('esc')
        time.sleep(2)
        pic_click_one('./gametimeline/Initiate_surrender.png', region=self.client_box)
        time.sleep(2)
        return pic_click_one('./gametimeline/surrender.png', region=self.client_box)

    def is_time_out(self):
        return time.time() - self.start_time > self.time_out

    def print_information(self):
        if time.time() - self.last_print_hero_list > 15:
            # log_print([[hero_dic['name'], hero_dic['num']] for hero_dic in self.hero_dic_list])
            # log_print([[fight_hero_pos.star,0][fight_hero_pos is None] for fight_hero_pos in self.fight_hero_pos_list])
            # log_print([hero_dic['star'] for hero_dic in self.hero_dic_list])
            self.last_print_hero_list = time.time()

    def base_hero_num(self):
        total = 0
        for hero_dic in self.hero_dic_list:
            if hero_dic['star'] > 0:
                total+=1
        return total

    def base_finish(self):
        finish = True
        for hero_dic in self.hero_dic_list:
            if hero_dic['star'] < 1:
                return False
        return True

    def find_finish(self):
        finish = True
        for hero_dic in self.hero_dic_list:
            if hero_dic['star'] < hero_dic['max_star']:
                finish = False
                if hero_dic['num'] <= 0:
                    hero_dic['num'] = 1
        return finish

    def is_game_over(self):
        x, y = pic_click_one('./gametimeline/drop_out.png', region=self.client_box)
        if x and y:
            return True
        # lol 游戏客户端消失 游戏结束
        if get_lol_client_hwnd() is None:
            return True
        return False

    @staticmethod
    def find_props_type(path_name_lsit, box=None):
        screenshotIm = pyscreeze.screenshot(region=None)
        result = []
        for path, name in path_name_lsit:
            props_box_list = locateAllOnScreen(path, screenshotIm, confidence=0.9, region=box)
            props_set = set()
            for props_box in props_box_list:
                x, y = props_box[0], props_box[1]
                props_set.add(Props_Pos(x, y))
            for i in range(len(props_set)):
                result.append(name)
                # break
        try:
            screenshotIm.fp.close()
        except AttributeError:
            pass
        return list(set(result))

    def find_props_info(self):
        self.props_info.init()
        props_dic = self.props_info.props_dic
        for index in range(len(props_xy_list)):
            x, y = props_xy_list[index]
            x += self.client_box[0]
            y += self.client_box[1]
            pyautogui.moveTo(x, y)
            time.sleep(0.1)
            props_type_arr = self.find_props_type(props_path_name_lsit, self.props_box)

            props_pos = Props_Pos(x, y)
            key = Props.get_key(props_type_arr)
            # log_print(key, end=',')
            # props_type_list[index] = key
            if key not in props_dic.keys():
                props_dic[key] = []
            props_dic[key].append(props_pos)
        self.click_space()
        # log_print()

    # ----------------------------------------------------------------------------------------------
    @staticmethod
    def find_hero_health_bar(box):
        # todo 根据线条前部+星级标志找
        box_list = tuple(pyautogui.locateAllOnScreen('./gametimeline/hero_health_bar.png', region=box, confidence=0.75))
        result = set()
        for b in box_list:
            result.add(Pos(b[0], b[1]))
        return result

    # index大于 人口时 找空位
    def find_vacancy(self, index, fight_num):
        if self.level > fight_num:
            return index

        for i in range(len(self.fight_hero_pos_list) - 1, self.level - 1, -1):
            if self.fight_hero_pos_list[i] is not None and i > index:
                return i
        return None

    # 获取英雄信息
    def get_hero_info_arr(self, box) -> list:
        result = self.find_hero_health_bar(box)
        hero_info_arr = []
        for pos in result:
            self.click_space()
            x, y = pos.x + 28, pos.y + 57
            pyautogui.mouseDown(x, y, button='right', duration=0.1)
            pyautogui.mouseUp(button='right')
            time.sleep(0.25)
            star, index, is_tibu = self.find_hero_info(x, y)
            # log_print('index %s. star %s. is_tibu %s.' % (str(index), str(star), str(is_tibu)))
            # 没有info界面
            if star is None:
                pass
            else:
                hero_pos = Hero_pos(index, star, Pos(x, y), is_tibu)
                hero_info_arr.append(hero_pos)
                self.update_hero_info(hero_pos)
        self.click_space()
        return hero_info_arr

    @staticmethod
    def close_screenshotIm(screenshotIm):
        try:
            screenshotIm.fp.close()
        except AttributeError:
            pass

    def find_hero_info(self, x=None, y=None):
        hero_info_box = self.client_box
        if x and y:
            hero_info_box = [x - 190, y - 100, 190 * 2, 250]
        # self.box_pic(hero_info_box, show=False)
        screenshotIm = pyscreeze.screenshot(region=None)
        star, index, is_tibu = None, None, False
        star = self.find_star(screenshotIm, hero_info_box)
        if star is None:
            # 没找到星级  表示没有info界面  不能判断是否卖掉英雄  只能返回true
            pass
        else:
            for i in range(len(self.hero_dic_list)):
                hero_dic = self.hero_dic_list[i]
                pos = locate(hero_dic['info_path'], screenshotIm, region=hero_info_box, confidence=0.95)
                if pos is not None:
                    index = i
                    break
                elif hero_dic['star'] <= 0:
                    for tibu in hero_dic['tibu_list']:
                        pos = locate(tibu['info_path'], screenshotIm, region=hero_info_box, confidence=0.95)
                        if pos is not None:
                            index = i
                            is_tibu = True
                            self.close_screenshotIm(screenshotIm)
                            return star, index, is_tibu
        self.close_screenshotIm(screenshotIm)
        return star, index, is_tibu

    def find_star(self, screenshotIm, box):
        for i in range(1, 4):
            star = locate('./gametimeline/star' + str(i) + '.png', screenshotIm, region=box, confidence=0.95)
            if star is not None:
                return i
        return None

    @staticmethod
    def in_box(x, y, x2, y2):
        w = 25
        return y - 50 <= y2 <= y + 65 and x - w <= x2 <= x + w

    def update_hero_info(self, hero_pos: Hero_pos):
        index, star, is_tibu = hero_pos.index, hero_pos.star, hero_pos.is_tibu
        if index is not None and not is_tibu:
            # 如果 星级达到最大星级  则把 数量置为0
            if star >= self.hero_dic_list[index]['max_star']:
                self.hero_dic_list[index]['num'] = 0
            self.hero_dic_list[index]['star'] = max(self.hero_dic_list[index]['star'], star)

    def check_fight_hero(self, sell=True):
        hero_info_arr = self.get_hero_info_arr(self.fight_box)
        self.fight_hero_pos_list = [None] * len(self.hero_dic_list)
        total = len(hero_info_arr)
        for info in hero_info_arr:
            index, star, pos, is_tibu = info.index, info.star, info.pos, info.is_tibu
            if index is None:
                self.sell_hero(pos.x, pos.y, sell)
                self.change_hero_status(pos.x, pos.y)
                total -= 1
                continue
            last_hero_pos = self.fight_hero_pos_list[index]
            if last_hero_pos is None:
                self.fight_hero_pos_list[index] = info
            else:
                if info.priority(last_hero_pos):
                    self.fight_hero_pos_list[index] = info
                    self.change_hero_status(last_hero_pos.pos.x, last_hero_pos.pos.y)
                    total -= 1
                else:
                    self.change_hero_status(pos.x, pos.y)
                    total -= 1

        # self.fight_hero_star_list = [None] * len(self.hero_dic_list)
        for hero_pos in self.fight_hero_pos_list:
            if hero_pos is None:
                continue
            index, star, pos, is_tibu = hero_pos.index, hero_pos.star, hero_pos.pos, hero_pos.is_tibu
            end_x, end_y = self.client_box[0] + fighting_hero_xy_list[index][0], \
                           self.client_box[1] + fighting_hero_xy_list[index][1],
            if not self.in_box(end_x, end_y, pos.x, pos.y):
                dragTo(end_x, end_y, startx=pos.x, starty=pos.y)
                pos.x, pos.y = end_x, end_y
                s = [' tibu dragTo ', ' dragTo '][is_tibu]
                # log_print(str(index) + s + str(index) + str(fighting_hero_xy_list[index]))
                time.sleep(0.1)
        return total

    def check_watch_hero(self, fight_num, sell=True):
        hero_info_arr = self.get_hero_info_arr(self.watch_box)
        for info in hero_info_arr:
            index, star, pos, is_tibu = info.index, info.star, info.pos, info.is_tibu
            if index is None:
                # 不要的牌 卖掉
                self.sell_hero(pos.x, pos.y, sell)
                continue

            fight_hero_pos = self.fight_hero_pos_list[index]
            target_hero_pos = self.hero_dic_list[index]['target']

            if info.priority(fight_hero_pos):
                # dragTo   交换 hero_pos   info <--> fight_hero_pos
                if fight_hero_pos is not None:
                    # 直接位置交换
                    idx = index
                elif self.level > fight_num:
                    # 有空位
                    idx = index
                    fight_num += 1
                else:
                    # 位置满了，试图寻找空位
                    idx = self.find_vacancy(index, fight_num)

                if idx is not None:
                    end_x, end_y = self.client_box[0] + fighting_hero_xy_list[idx][0], \
                                   self.client_box[1] + fighting_hero_xy_list[idx][1],
                    if not self.in_box(end_x, end_y, pos.x, pos.y):
                        dragTo(end_x, end_y, startx=pos.x, starty=pos.y)
                        s = ' tibu dragTo ' if is_tibu else ' dragTo '
                        # log_print(str(index) + s + str(idx) + str(fighting_hero_xy_list[idx]))
                        self.fight_hero_pos_list[index] = None
                        info.pos.x, info.pos.y = end_x, end_y
                        self.fight_hero_pos_list[idx] = info
                        time.sleep(0.1)
                        if idx != index:
                            end_x, end_y = self.client_box[0] + fighting_hero_xy_list[index][0], \
                                           self.client_box[1] + fighting_hero_xy_list[index][1],
                            time.sleep(0.5)
                            dragTo(end_x, end_y)
                            self.fight_hero_pos_list[idx] = None
                            info.pos.x, info.pos.y = end_x, end_y
                            self.fight_hero_pos_list[index] = info
                            time.sleep(0.1)

            elif is_tibu and fight_hero_pos.is_tibu:
                self.sell_hero(pos.x, pos.y, sell)
            elif fight_hero_pos.pri_and_eq(target_hero_pos):
                self.sell_hero(pos.x, pos.y, sell)
        return fight_num

    def check_all_hero(self, sell=True):
        # 是否有英雄需要的装备
        fight_num = self.check_fight_hero(sell=sell)
        # todo 限定时间  放在别的位置
        self.find_props_info()
        # log_print(self.props_info.hero_need_props_info.keys())
        # log_print(self.props_info.props_dic.keys())
        self.props_info.have_props_to_hero()

        return self.check_watch_hero(fight_num, sell=sell)

    # ----------------------------------------------------------------------------------------------
    def check_level(self):
        for round_target_level in self.round_target_level_list:
            rd, target_level = round_target_level[0], round_target_level[1]
            if self.round >= rd and self.level < target_level and self.gold >= self.check_level_threshold:
                self.upgrade_champ()
                return True
        return False

    # ----------------------------------------------------------------------------------------------
    # 根据 给的box, 在box中识别 lib_list中的图片 并转化未相应的字符
    # lib_list [ 图片，  找到图片后对应的字符 ]
    @staticmethod
    def ocr(box, lib_list, show=False, confidence=0.95, threshold=None, screenshotIm=None):
        if screenshotIm is not None:
            pic = screenshotIm
        else:
            pic = pyscreeze.screenshot(region=None)

        if show:
            pic.show()

        if threshold:
            pic = Game_Timeline.convert_2(pic, threshold=threshold)

        list = []
        for path_and_name in lib_list:
            path = path_and_name[0]
            name = path_and_name[1]
            points = tuple(pyscreeze.locateAll(path, pic, confidence=confidence, region=box))
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
            if screenshotIm is None:
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
    def box_pic(box, show=True):
        pic = pyscreeze.screenshot(region=box)
        if show:
            pic.show()
        pic.save('./daibi.png')
        try:
            pic.fp.close()
        except Exception:
            pass

    # 识别 等级，回合、金币--------------------------------------------------------------------------------------
    def update_gold(self, screenshotIm=None):
        gold = self.ocr_gold(screenshotIm=screenshotIm)
        if gold is not None:
            g = self.str_to_int(gold)
            if g != self.gold:
                self.gold = g
                log_print('gold: '+str(self.gold))
        return self.gold

    def ocr_gold(self, screenshotIm=None):
        return self.ocr(self.gold_box, gold_lib_list, screenshotIm=screenshotIm)

    def update_level(self, screenshotIm=None):
        level = self.ocr_level(screenshotIm=screenshotIm)
        if level is not None:
            lv = self.str_to_int(level)
            if lv > self.level:
                self.level = lv
                log_print('level: '+str(self.level))
        return self.level

    def ocr_level(self, screenshotIm=None):
        return self.ocr(self.level_box, level_lib_list, screenshotIm=screenshotIm)

    # 每次到达新的回合，sleep
    def update_round(self, screenshotIm=None):
        draft = self.ocr_round(screenshotIm=screenshotIm)
        if draft is not None:
            d = self.str_to_int(draft)
            if d > self.round:
                self.round = d
                time.sleep(1)
                log_print('round: '+str(int(self.round / 10))+'-'+str(int(self.round % 10)))
                return self.round
        return None

    def ocr_round(self, screenshotIm=None):
        return self.ocr(self.round_box, draft_lib_list, screenshotIm=screenshotIm)

    def update_round_level_gold(self):
        screenshotIm = pyscreeze.screenshot(region=None)
        update_round = self.update_round(screenshotIm=screenshotIm)
        update_level = self.update_level(screenshotIm=screenshotIm)
        update_gold = self.update_gold(screenshotIm=screenshotIm)
        try:
            screenshotIm.fp.close()
        except Exception:
            return update_round, update_level, update_gold
        return update_round, update_level, update_gold

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
        click(self.client_box[0] + 140 + random.randint(-10,0), self.client_box[1] + 400 + random.randint(-20,0))
        if right:
            click(self.client_box[0] + 140, self.client_box[1] + 400, button='right')

    # -----------------------------------------------------------------------------------------------------------
    @staticmethod
    def sell_hero(x, y, sell=True):
        if sell:
            pyautogui.mouseDown(x, y, button='left')
            slow_key_press('e')
            time.sleep(0.1)
            pyautogui.mouseUp(button='left')

    # 上场下场英雄
    @staticmethod
    def change_hero_status(x, y):
        pyautogui.moveTo(x, y)
        slow_key_press('w')


def find_card(game_timeline: Game_Timeline, region=None):
    total = 0
    screenshotIm = pyscreeze.screenshot(region=None)

    for hero_dic in game_timeline.hero_dic_list:
        click_num = pic_click_all(hero_dic['path'], max_click=hero_dic['num'], region=region, screenshotIm=screenshotIm)
        if click_num > 0:
            # log_print('click ' + hero_dic['name'] + ' ' + str(click_num))
            hero_dic['num'] = hero_dic['num'] - click_num
        if hero_dic['star'] <= 0 and click_num <= 0:
            for tibu in hero_dic['tibu_list']:
                click_num = pic_click_all(tibu['path'], max_click=tibu['num'], region=region, screenshotIm=screenshotIm)
                if click_num > 0:
                    # log_print('click ' + hero_dic['name'] + ' tibu ' + tibu['name'])
                    tibu['num'] = tibu['num'] - click_num
        total += click_num
    try:
        screenshotIm.fp.close()
    except AttributeError:
        pass
    return total


def search_hero(game_timeline: Game_Timeline):
    return find_card(game_timeline, region=game_timeline.find_hero_box)


def can_run_(current_time):
    for run_time in run_datetime_list:
        if run_time.canRun(current_time):
            return True
    return False


def change_game_status():
    global autoPaly
    autoPaly = not autoPaly
    log_print('change_game_status.  ' + ('running' if autoPaly else 'stop'))
    return autoPaly


def stop_game():
    global stop
    stop = not stop
    log_print(['running', 'stop'][stop])
    return stop


keyboard.add_hotkey('F12', change_game_status)
keyboard.add_hotkey('F11', stop_game)


def func_keep_find(game_timeline):
    if game_timeline.find_finish():
        return True


def func_keep_fast_find(game_timeline):
    if game_timeline.find_finish():
        return True
    if game_timeline.can_fast_find():
        search_hero(game_timeline)
        refresh_shop()
        search_hero(game_timeline)
        game_timeline.print_information()
    return True


def func_wait_game_over(game_timeline):
    pass


def func_1_3_normal(game_timeline):
    if len(game_timeline.find_hero_health_bar(game_timeline.client_box)) < 2:
        if search_hero(game_timeline) <= 0:
            pic_click_one('./role/fee1.png')


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
    Game('./gametimeline/game_1_3.png', 13, func_1_3_normal, func_keep_fast_find),
    Game('./gametimeline/drop_out.png', 999, func_wait_game_over, func_keep_fast_find)
]

formation = None


def probability(probability_list):
    total = 0
    rand_num = random.random() * sum(probability_list)
    for index in range(len(probability_list)):
        total += probability_list[index]
        if rand_num<total:
            return index
    return len(probability_list)-1


def init_Formation():
    global yaml_data
    yaml_data = get_yaml_data('data.yaml')
    global formation
    Formation_list = yaml_data['Formation']
    formation_probability = yaml_data['formation_probability']
    index = probability(formation_probability)
    formation = Formation_list[index]
    global fighting_hero_xy_list
    fighting_hero_xy_list = []
    for hero in formation:
        fighting_hero_xy_list.append(fight_xy_list[hero['pos']])
    global props_path_name_lsit
    props_path_name_lsit = []
    for filename in os.listdir(r'./gametimeline/props'):
        name = filename.split('.png')[0]
        props_path_name_lsit.append(['./gametimeline/props/' + filename, name])


def init_hero_dic_list()->list:
    global formation
    index = 0
    for hero in formation:
        hero['path'] = './role/' + hero['name'] + '.png'
        hero['info_path'] = './role/roleinfo/' + hero['name'] + '.png'
        hero['star'] = 0
        hero['target'] = Hero_pos(index, hero['max_star'], None, False)
        for tibu in hero['tibu_list']:
            tibu['path'] = './role/' + tibu['name'] + '.png'
            tibu['info_path'] = './role/roleinfo/' + tibu['name'] + '.png'
            tibu['star'] = 0

        index += 1
    return formation


# watch_hero_xy_list = [
#     [576, 660], [662, 660], [743, 660], [827, 660], [908, 660]
#     , [992, 660], [1075, 660], [1156, 660], [1239, 660]
# ]

# 观赛席 相对box的坐标
watch_hero_xy_list = [[124, 549], [215, 549], [301, 549], [385, 549], [466, 549], [550, 549], [633, 549], [717, 549],
                      [800, 549]]

fighting_hero_xy_list = [
    [518, 472], [475, 419], [519, 365],
    [610, 474], [560, 416], [602, 368],
    [693, 476], [650, 416], [686, 363]
]
fight_xy_list = [
    #    0          1            2           3           4            5            6
    [230, 325], [314, 325], [394, 325], [476, 325], [555, 325], [639, 325], [716, 325],
    #    7           8           9           10          11           12           13
    [267, 375], [351, 375], [433, 375], [517, 375], [599, 375], [682, 375], [764, 375],
    #    14          15          16          17          18           19           20
    [213, 428], [299, 428], [386, 428], [471, 428], [559, 428], [646, 428], [733, 428],
    #    21          22          23          24          25           26           27
    [246, 486], [336, 486], [426, 486], [517, 486], [608, 486], [694, 486], [786, 486]
]


props_xy_list = [
    [47, 549], [61, 503], [70, 460], [116, 475], [110, 465], [142, 475]
]
props_xy_list = [[35, 555], [76, 546], [40, 513], [82, 504], [51, 478], [120, 501], [108, 475], [64, 447], [146, 473],
                 [108, 443]]

props_path_name_lsit = []


# ------------------------------------------------------------------------------------------------------------------
autoPaly = True
stop = False
print('start.')
time.sleep(1)

num = 1


def stop_game():
    global autoPaly
    autoPaly = False


def run_game():
    global autoPaly
    autoPaly = True


def main():
    global num
    while True:
        pyautogui.moveTo(100, 100)
        while autoPaly:
            ckeck_time()

            activate_client()

            # 判断进入哪个分支
            #     open_game()
            time.sleep(1)
            pic_click_one('./gametimeline/OK.png', confidence=0.7)
            log_print('status')
            if get_lol_hwnd() is not None:
                log_print('open_game')
                open_game(lol_hwnd=get_lol_hwnd())
            elif get_lol_client_hwnd() is not None:
                if pic_exists('./gametimeline/In_game_logo.png', confidence=0.7):
                    os.system('taskkill /IM TenioDL.exe /F')
                    init_Formation()
                    log_print(formation)
                    log_print(fighting_hero_xy_list)
                    log_print('play_game = '+str(num), end=' ')
                    log_print(datetime.datetime.now().strftime("%Y--%m--%d %H:%M:%S"))
                    Game_Timeline(normal_game_execute_list).run()
                    num = num + 1
                    time.sleep(120+random.randint(0,60))
                else:
                    log_print('loading')
            else:
                pic_click_one('./gametimeline/OK.png', confidence=0.7)

            time.sleep(3)

        time.sleep(5)


formation_probability = yaml_data['formation_probability']
da = [0] * len(formation_probability)
tttt = 1000
while tttt>0:
    index = probability(formation_probability)
    da[index]+=1
    tttt-=1
    print(index)
print(da)
