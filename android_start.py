import time
import traceback
import random
import pyautogui


def game_state():
    """
    判断游戏界面属于什么状态
    """
    if pic_exits('./android_start/out_game.png', '未开标志图片0'):
        print('游戏未开状态')
        return 0
    elif pic_exits('android_start/in_game.png', '游戏中图片1'):
        print('云顶游戏中状态')
        return 1
    else:
        print('没找到对应的状态图片')
        return 3


def wait_pic_load(pic_path, tag, max_wait):
    wait_count = 0
    while True:
        if wait_count >= max_wait:
            print("未找到" + tag + "图片坐标")
            return False, None, None
        buttonx, buttony = find_pic(pic_path, tag)
        if buttonx and buttony:
            print("找到" + tag + "图片坐标", buttonx, buttony)
            return True, buttonx, buttony
        else:
            time.sleep(1)
            wait_count += 1


def pic_exits(pic_path, tag):
    try:
        buttonx, buttony = pyautogui.locateCenterOnScreen(pic_path, confidence=0.85)
        if buttonx and buttony:
            print("找到" + tag + "图片坐标", buttonx, buttony)
            return True
        else:
            print("寻找" + tag + "图片失败", buttonx, buttony)
            return False
    except Exception as e:
        # print(str(e))
        print("寻找" + tag + "图片失败")
        return False


def find_pic(pic_path, tag):
    try:
        buttonx, buttony = pyautogui.locateCenterOnScreen(pic_path, confidence=0.85)
        print("找到" + tag + "图片坐标", buttonx, buttony)
        return buttonx, buttony
    except Exception as e:
        # print(traceback.print_exc())
        print("找到" + tag + "图片失败")
        return None, None


def find_pic_play(pic_path, tag, sleep=3, duration=0.1):
    try:
        buttonx, buttony = find_pic(pic_path, tag)
        if buttonx and buttony:
            pyautogui.click(buttonx, buttony, duration=duration)
            pyautogui.sleep(sleep)
            return True
    except Exception as e:
        # print(traceback.print_exc())
        print(str(e))
        return False


def find_pic_move_to(pic_path, tag, sleep=3):
    try:
        buttonx, buttony = find_pic(pic_path, tag)
        if buttonx and buttony:
            pyautogui.moveTo(buttonx, buttony)
            time.sleep(sleep)
            return True
    except Exception as e:
        # print(traceback.print_exc())
        print(str(e))
        return False


def find_click_pick_lol(pic_path, tag):
    try:
        x, y = find_pic(pic_path, tag)
        if x and y:
            pyautogui.moveTo(x, y)
            pyautogui.mouseDown()
            pyautogui.mouseUp()
            return True
        return False
    except Exception as e:
        print(str(e))
        return False


def open_lol_game():
    pyautogui.click(850,300)
    time.sleep(1)
    find_click_pick_lol('./android_start/play_again.png','再玩一次')
    if find_pic_play('./android_start/search_game.png', '寻找对局'):
        isfind, bx, by = wait_pic_load('./android_start/ac_game.png', '接受对局', 60)
        if isfind:
            pyautogui.click(bx, by)


def pick_up():
    time.sleep(1)
    check_left_right(left=False)
    time.sleep(1)
    pyautogui.click(1320, 522)
    time.sleep(4)
    pyautogui.click(1132, 307)
    time.sleep(3)
    check_left_right(left=True)


def play_game_ing():
    xy = [[753, 914],
     [595, 942],
     [980, 942],
     [1166, 942],
     [1348, 942],

     [400, 922],
     [420, 998]]

    while True:
        x,y = random.choice(xy)
        x +=random.randint(-20,20)
        y +=random.randint(-20,20)
        pyautogui.click(x,y,duration=0.2)
        if find_click_pick_lol('./android_start/game_over.png', '游戏退出'):
            for i in range(3):
                time.sleep(1)
                find_click_pick_lol('./android_start/game_over.png', '游戏退出')
            print('游戏结束')
            break
        if game_state() != 1:
            break
        pick_up()
        time.sleep(3)
    time.sleep(120+random.randint(0,60))


def check_left_right(left):
    l = False
    if pic_exits('./android_start/left_mouse.png','左键状态'):
        l = True
    if l ^ left:
        pyautogui.click(113,285)


if __name__ == '__main__':
    time.sleep(5)

    while True:
        state = game_state()
        check_left_right(left=True)
        if state == 0:
            open_lol_game()
        elif state == 1:
            play_game_ing()
        else:
            find_click_pick_lol('./android_start/OK.png','OK')
            pass
        time.sleep(5)
