import cv2
import pyautogui
import pyscreeze
import numpy as np
import time


def generate_alpha(alpha_channel, last_channel, curr_channel, confidence=0.999):
    threshold = int(255 * (1 - confidence))
    for i in range(last_channel.shape[0]):
        for j in range(last_channel.shape[1]):
            alpha_channel[i, j] = alpha_channel[i, j] if abs(
                int(curr_channel[i, j]) - int(last_channel[i, j])) <= threshold else 0


def qubeijing_for_time(sec_time, box, file_path_name, confidence=0.999):
    last_template = None
    alpha_channel = None
    start_time = time.time()
    region = [box[0], box[1], box[2] - box[0], box[3] - box[1]]
    while time.time() - start_time < sec_time:
        # box 要为元组 (870,500,1000,600)
        screenshotIm = pyscreeze.screenshot(region=region)
        template = pyscreeze._load_cv2(screenshotIm)
        close_screenshotIm(screenshotIm)
        b_channel, g_channel, r_channel = cv2.split(template)
        if alpha_channel is None:
            alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255
        if last_template is not None:
            b, g, r = cv2.split(last_template)
            generate_alpha(alpha_channel, b_channel, b, confidence=confidence)
            generate_alpha(alpha_channel, g_channel, g, confidence=confidence)
            generate_alpha(alpha_channel, r_channel, r, confidence=confidence)
        last_template = template
    b_channel, g_channel, r_channel = cv2.split(last_template)
    img_BGRA = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))
    # alpha = template[:,:,3]
    cv2.imwrite(file_path_name, img_BGRA)


def qubeijing_for_pic_list(pic_list, file_path_name, confidence=0.999):
    last_template = None
    alpha_channel = None
    start_time = time.time()
    for pic in pic_list:
        template = pyscreeze._load_cv2(pic)
        b_channel, g_channel, r_channel = cv2.split(template)
        if alpha_channel is None:
            alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255
        if last_template is not None:
            b, g, r = cv2.split(last_template)
            generate_alpha(alpha_channel, b_channel, b, confidence=confidence)
            generate_alpha(alpha_channel, g_channel, g, confidence=confidence)
            generate_alpha(alpha_channel, r_channel, r, confidence=confidence)
        last_template = template
    b_channel, g_channel, r_channel = cv2.split(last_template)
    img_BGRA = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))
    # alpha = template[:,:,3]
    cv2.imwrite(file_path_name, img_BGRA)


def close_screenshotIm(screenshotIm):
    try:
        screenshotIm.fp.close()
    except AttributeError:
        pass


def find_touming(path, confidence=0.95):
    t2 = cv2.imread(path)
    alpha = cv2.imread(path, cv2.IMREAD_UNCHANGED)[:, :, 3]
    screenshotIm = pyscreeze.screenshot(region=None)
    result = cv2.matchTemplate(pyscreeze._load_cv2(screenshotIm), t2, cv2.TM_CCORR_NORMED, mask=alpha)

    # 获取结果中最大值和最小值以及他们的坐标
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    pyautogui.moveTo(max_loc[0], max_loc[1])
    print(max_val)

    close_screenshotIm(screenshotIm)

    if max_val > confidence:
        return (max_loc[0], max_loc[1])
    else:
        return None


if __name__ == '__main__':
    pic_list = [
        './pic_rank/bobi.png',
        './pic_rank/kelie.png',
        './pic_rank/zhadanren.png',
        './pic_rank/lulu.png',
        './pic_rank/kainan.png',
    ]
    qubeijing_for_pic_list(pic_list, 'mask_2.png',confidence=0.95)

    find_touming('mask_2.png')
# ImageGrab.grab((870,500,1000,600)).show()
