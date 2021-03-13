from PIL import Image as IMG, ImageEnhance
from io import BytesIO
from numba import jit
import numpy as np


np.seterr(divide="ignore", invalid="ignore")

# 感谢老司机
# https://zhuanlan.zhihu.com/p/31164700
def gray_car(wimg: bytes, bimg: bytes,
	wlight: float = 1.0, blight: float = 0.3, chess: bool = False):
    """
    发黑白车
    :param wimg: 白色背景下的图片
    :param bimg: 黑色背景下的图片
    :param wlight: wimg 的亮度
    :param blight: bimg 的亮度
    :param chess: 是否棋盘格化
    :return: 处理后的图像
    """
    wimg = IMG.open(BytesIO(wimg))
    bimg = IMG.open(BytesIO(bimg))
    size = max(wimg.size[0], bimg.size[0]), max(wimg.size[1], bimg.size[1])
    return IMG.fromarray(build_car(
        np.array(wimg.convert("L").resize(size)).astype("float64"),
        np.array(bimg.convert("L").resize(size)).astype("float64"),
        chess, wlight, blight
        ), "RGBA")

# 用jit一时爽，一直用一直爽
# (如果你的py版本/系统不支持numba,把这个修饰器和上面的import删了即可)
def build_car(wpix, bpix, wlight, blight, chess):
    # 棋盘格化
    # 规则: if (x + y) % 2 == 0 { wpix[x][y] = 255 } else { bpix[x][y] = 0 }
    if chess:
        wpix[::2, ::2] = 255.0
        bpix[1::2, 1::2] = 0.0

    wpix *= wlight
    bpix *= blight

    a = 1.0 - wpix / 255.0 + bpix / 255.0
    r = np.where(a != 0, bpix / a, 255.0)

    pixels = np.dstack((r, r, r, a * 255.0))

    pixels[pixels > 255] = 255
    # return pixels.astype("uint8")
    return pixels.astype("uint8")

import time
from pathlib import Path
t=time.time()
gray_car(
    Path('2020-11-25_21.49.01_2756804290.jpeg').read_bytes(),
    Path('2020-11-26_07.39.07_2324366206.jpeg').read_bytes()).save('a.png')
print(time.time()-t)