import os

import numpy
import pyautogui
import time
import pyscreeze
import psutil
from PIL import Image
import cv2


def get_win_hwnd(title):
    try:
        w = pyautogui.getWindowsWithTitle(title)
        for i in w:
            if i.title == title:
                return i
        return None
    except Exception as e:
        return None


def get_lol_client_hwnd():
    return get_win_hwnd('League of Legends (TM) Client')


def ocr(box, font_library_path, show=False):
    pic = pyscreeze.screenshot(region=box)
    if show:
        pic.show()
    list = []
    # todo
    for filename in os.listdir(font_library_path):
        points = tuple(pyscreeze.locateAll(font_library_path + filename, pic, confidence=0.97))
        if len(points):
            for point in points:
                list.append((point[0], filename[:filename.rindex('.')]))
    list.sort()
    s = ''
    for n in list:
        s += str(n[1])
    # num = None
    try:
        # num = int(s)
        pic.fp.close()
    except Exception:
        pass
    return s


def ocr_2(box, font_library_path, show=False, threshold=[160, 190], confidence=0.8, pic_path=None):
    if pic_path:
        pic = Image.open(pic_path)
    else:
        pic = pyscreeze.screenshot(region=box)
    pic = convert_2(pic, threshold)
    if show:
        pic.show()
    list = []

    for filename in os.listdir(font_library_path):
        points = tuple(pyscreeze.locateAll(font_library_path + filename, pic, confidence=confidence))
        if len(points):
            for point in points:
                list.append((point[0], filename[:filename.rindex('.')]))
    list.sort()
    s = ''
    for n in list:
        s += str(n[1])
    # num = None
    try:
        # num = int(s)
        pic.fp.close()
    except Exception:
        pass
    return s


def box_pic(box):
    pic = pyscreeze.screenshot(region=box)
    pic.show()
    pic.save('./daibi.png')
    try:
        pic.fp.close()
    except Exception:
        pass


def ocr_gold(box):
    s = ocr(box, './gametimeline/gold/')
    num = None
    try:
        num = int(s)
    except Exception:
        pass
    return num


# 快速计算box
def jisuan(point):
    print(point[0] - 445, point[1] - 121, point[2] - point[0], point[3] - point[1])


watch_hero_xy_list = [
    [576, 660], [662, 660], [743, 660], [827, 660], [908, 660]
    , [992, 660], [1075, 660], [1156, 660], [1239, 660]
]

watch_hero_xy_list = [[124, 549], [215, 549], [301, 549], [385, 549], [466, 549], [550, 549], [633, 549], [717, 549],
                      [800, 549]]

# print([[i[0],i[1]+20] for i in watch_hero_xy_list])
# jisuan([466, 769, 505, 793])
while False:
    time.sleep(2)
    box = pyautogui.locateOnScreen('./gametimeline/title.png')
    # box = get_lol_client_hwnd().box
    if box:
        # 回合
        print('draft:' + ocr([box[0] + 365, box[1] + 25, 35, 27], 'gametimeline/draft/', show=False))
        #
        # # 金币
        # print('gold:'+ocr([box[0] + 432, box[1] + 646, 52, 34], './gametimeline/gold/', show=False))
        # #
        # print('level:'+ocr([box[0] + 21, box[1] + 648, 39, 24], './gametimeline/level/', show=False))

        # find_hero_box = [box[0] + 166, box[1] + 680, 724, 112]
        # box_pic(find_hero_box)


def cmp(a, b):
    return abs(a[0] - b[0]) < 30 and abs(a[1] - b[1]) < 20


class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return abs(self.x - other.x) < 30 and abs(self.y - other.y) < 20

    def __lt__(self, other):
        if abs(self.x - other.x) < 30:
            return self.y + 20 < other.y
        return self.x + 30 < other.x

    def __hash__(self):
        return 0

    # def __cmp__(self, other):


class Hero:
    def __init__(self, hero):
        self.name = hero['name']
        self.pic = './role/' + hero['name'] + '.png'
        self.info = './roleinfo/' + hero['name'] + '.png'

        self.is_fight = False
        self.watch = []
        self.num = 0


# get_win_hwnd('d')

# print(pyautogui.locateOnScreen('./gametimeline/hero_health_bar.png',confidence=0.99))
# print(pyscreeze.locate(Image.open('./579.png'), Image.open('./daibi3.png')))
# img = Image.open('./579.png')
# print()


def convert_2(img, threshold=[0, 255]):
    # img = Image.open(img_path)
    img = img.convert('L')
    # img.show()
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


def check_hero(box):
    box_list = pyautogui.locateAllOnScreen('./gametimeline/hero_health_bar.png', region=box, confidence=0.8)
    result = set()
    for b in box_list:
        result.add(Pos(b[0], b[1]))
    print(len(result))
    for p in result:
        pyautogui.mouseDown(p.x + 25, p.y + 53, button='right', duration=0.1)
        pyautogui.mouseUp(p.x + 25, p.y + 53, button='right', duration=0.1)
        time.sleep(0.7)


def click(x, y):
    pyautogui.mouseDown(x, y, duration=0.1)
    pyautogui.mouseUp(x, y, duration=0.1)

time.sleep(2)


    # time.sleep(3)
# print(pyautogui.locateOnScreen('./role/T-xinghong.png', confidence=0.95))
# li = []
# for i in [965, 593], [921, 537], [964, 489], [1053, 593], [1005, 537], [1047, 489]:
#     li.append([i[0]-445,i[1]-121])
# print(li)
# box = pyautogui.locateOnScreen('./gametimeline/searching_game.png', confidence=0.7)
# print(box)
# if box:
#     click(box[0] + 202, box[1] + 14)
#     time.sleep(1)
#     click(box[0] + 202, box[1] + 14)
#     click(box[0] + 202, box[1] + 14)


#
# pic = Image.open('./play.png')
# pic.show()


# box = pyautogui.locateOnScreen('./client/daibi.png', confidence=0.95)
# if box:
#     box = [box[0], box[1], 68, 68]
#
# print(ocr_2(box, './client/daibi/', show=False, threshold=[160, 190], confidence=0.80
#             # ,pic_path='./21.png'
#             ))

# Image.
# convert_2(Image.open('./daibi2.png'), [140, 200])

# pids = psutil.pids()
# for pid in pids:
#     p = psutil.Process(pid)
#     # get process name according to pid
#     process_name = p.name()
#
#     print("Process name is: %s, pid is: %s" % (process_name, pid))


# get_lol_client_hwnd().restore()
# get_lol_client_hwnd().activate()
# time.sleep(1)

# box = pyautogui.locateOnScreen('./gametimeline/title.png')
# if box:
#     fight_box = [box[0] + 28, box[1] + 158, 890, 305]
#     watch_box = [box[0] + 28, box[1] + 158 + 305, 890, 150]
#     check_hero(fight_box)
#     check_hero(watch_box)

# a = set()
#
# a.add(Pos(122, 10))
# a.add(Pos(132, 50))
# a.add(Pos(132, 15))
# a.add(Pos(132, 120))
# a.add(Pos(200, 17))
# for i in a:
#     print((i.x,i.y))


# s = './asdasdas/asdasd/dashu.png'
# print(s[s.rindex('/')+1:s.rindex('.')])
# hero_list = [['./asdasd/dashu.png',1],['./asdasd/xiaopao.png',1],['./asdasd/maomi.png',1]]
# print([[hero[0][hero[0].rindex('/')+1:hero[0].rindex('.')],hero[1]] for hero in hero_list])
# # print(jisuan([500, 595, 1331, 738]))

# box_pic([1,600,200,200])
# box = pyautogui.locateOnScreen('./gametimeline/hero_health_bar.png',region=[1,500,200,800],confidence=0.90)
# print(box)
# pyautogui.click(box[0] + 23, box[1] + 40)

# time.sleep(2)


# print(pyautogui.locateCenterOnScreen('./gametimeline/mark_waiting_game.png', confidence=0.7))


# import ctypes
#
# ahk = ctypes.cdll.AutoHotkey

# pyclient = ctypes.create_string_buffer("ahkpython.ahk")  # no unicode in ahk
# CMPFUNC = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int)
#
#
# def py_cmp_func(a):
#     print("ahk: ", a)
#     return a
#
#
# # for c in 'qq877726913..':
# #     print('send, {'+c+' down}')
# #     print('sleep, 1000')
# #     print('send, {' + c + ' up}')
# #     print('sleep, 1000')
# #
# cmp_func = CMPFUNC(py_cmp_func)
# fx = ctypes.create_string_buffer(str(ctypes.cast(cmp_func, ctypes.c_void_p).value))
# script = ctypes.create_string_buffer("""
# fx2(msg){
# WinActivate %msg%
# msgbox in function fx2 with %msg% from python
# return "success"
# }
# """)
# ahk.ahkdll(pyclient, "", fx)
# ahk.ahkassign(ctypes.create_string_buffer("fx"), fx)
# ahk.addScript(script)
# ahk.ahkFunction(ctypes.create_string_buffer("fx2"), ctypes.create_string_buffer("Untitled"))
