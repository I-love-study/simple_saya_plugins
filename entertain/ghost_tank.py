from graia.application import GraiaMiraiApplication
from graia.application.event.messages import GroupMessage
from graia.application.message.elements.internal import Plain, Image
from graia.application.message.chain import MessageChain
from graia.application.message.parser.kanata import Kanata
from graia.application.message.parser.signature import FullMatch, RequireParam
from graia.application.group import Group, Member

from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

from PIL import Image as IMG, ImageEnhance
from io import BytesIO
import numpy as np


np.seterr(divide="ignore", invalid="ignore")

channel = Channel.current()

channel.name("GhostTank")
channel.description("发送'ghost_tank [图][图]'获取幻影坦克黑白图")
channel.author("I_love_study")

@channel.use(ListenerSchema(
	listening_events=[GroupMessage],
	inline_dispatchers=[Kanata([FullMatch('ghost_tank'), RequireParam('para')])]
	))
async def ghost_tank(app: GraiaMiraiApplication, group: Group, member: Member, para: MessageChain):
	if len(p := messages.get(Image)) == 2:
		pics = asyncio.gather(*[i.http_to_bytes() for i in p])
		b = bytesIO()
		gray_car(*pics).save(b, format='PNG')
		await app.sendGroupMessage(group, MessageChain.create([Image.fromUnsafeBytes(b.getvalue())]))
	else:
		await app.sendGroupMessage(group, MessageChain.create([Plain('你这图,数量不对啊kora')]))

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
    return Image.fromarray(build_car(
        np.array(wimg.convert("L").resize(size)).astype("float64"),
        np.array(bimg.convert("L").resize(size)).astype("float64"),
        chess, wlight, blight
        ), "RGBA")

#本想着整个jit加速，后面发现压根没加速(悲)
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

    return pixels.astype("uint8")