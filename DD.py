# from ctypes import *
#
# import time
#
# # 注册DD DLL，64位python用64位，32位用32位，具体看DD说明文件。
# # 测试用免安装版。
# # 用哪个就调用哪个的dll文件。
# dd_dll = windll.LoadLibrary('ddx64.dll')
#
# # DD虚拟码，可以用DD内置函数转换。
# vk = {'5': 205, 'c': 503, 'n': 506, 'z': 501, '3': 203, '1': 201, 'd': 403, '0': 210, 'l': 409, '8': 208, 'w': 302,
#       'u': 307, '4': 204, 'e': 303, '[': 311, 'f': 404, 'y': 306, 'x': 502, 'g': 405, 'v': 504, 'r': 304, 'i': 308,
#       'a': 401, 'm': 507, 'h': 406, '.': 509, ',': 508, ']': 312, '/': 510, '6': 206, '2': 202, 'b': 505, 'k': 408,
#       '7': 207, 'q': 301, "'": 411, '\\': 313, 'j': 407, '`': 200, '9': 209, 'p': 310, 'o': 309, 't': 305, '-': 211,
#       '=': 212, 's': 402, ';': 410}
# # 需要组合shift的按键。
# vk2 = {'"': "'", '#': '3', ')': '0', '^': '6', '?': '/', '>': '.', '<': ',', '+': '=', '*': '8', '&': '7', '{': '[',
#        '_': '-',
#        '|': '\\', '~': '`', ':': ';', '$': '4', '}': ']', '%': '5', '@': '2', '!': '1', '(': '9'}
#
#
# def down_up(code):
#     # 进行一组按键。
#
#     dd_dll.DD_key(vk[code], 1)
#     dd_dll.DD_key(vk[code], 2)
#
#
# def dd(key):
#     # 500是shift键码。
#     if i.isupper():
#         # 如果是一个大写的玩意。
#
#         # 按下抬起。
#         dd_dll.DD_key(500, 1)
#         down_up(i.lower())
#         dd_dll.DD_key(500, 2)
#
#     elif i in '~!@#$%^&*()_+{}|:"<>?':
#         # 如果是需要这样按键的玩意。
#         dd_dll.DD_key(500, 1)
#         down_up(vk2[i])
#         dd_dll.DD_key(500, 2)
#     else:
#         down_up(i)
#
#
# input("按任意键继续...")
# # 之后等待两秒。
# time.sleep(2)
#
# # 测试按键。
# for i in 'http://www.ddxoft.com':
#     dd(i)