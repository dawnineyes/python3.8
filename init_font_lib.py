import os


def init_lib(list, lib_path):
    for filename in os.listdir(lib_path):
        list.append([lib_path + filename, filename[:filename.rindex('.')]])


def init_level_lib_list():
    level_lib_list = []
    # 初始化等级字体库
    level_lib_path = './gametimeline/level/'
    init_lib(level_lib_list, level_lib_path)
    return level_lib_list


# 初始化 金币字体库
def init_gold_lib_list():
    gold_lib_list = []
    gold_lib_path = './gametimeline/gold/'
    init_lib(gold_lib_list, gold_lib_path)
    return gold_lib_list


def init_draft_lib_list():
    draft_lib_list = []
    draft_lib_path = './gametimeline/draft/'
    init_lib(draft_lib_list, draft_lib_path)
    return draft_lib_list


def init_daibi_lib_list():
    daibi_lib_list = []
    daibi_lib_path = './client/daibi/'
    init_lib(daibi_lib_list, daibi_lib_path)
    return daibi_lib_list
