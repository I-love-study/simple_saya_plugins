from graia.application import GraiaMiraiApplication
from graia.application.event.messages import GroupMessage
from graia.application.message.elements.internal import Plain, Image
from graia.application.message.chain import MessageChain
from graia.application.message.parser.kanata import Kanata
from graia.application.message.parser.signature import FullMatch, RequireParam
from graia.application.group import Group, Member
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
import aiohttp, urllib
from lxml import etree

headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                       'Chrome/81.0.4044.69 Safari/537.36 Edg/81.0.416.34'}

channel = Channel.current()

channel.name("BaiduSearch")
channel.description("发送'百科 [词语]'获取拜读百科词条\n发送热点获取百度热点Top10")
channel.author("I_love_study")

@channel.use(ListenerSchema(
    listening_events=[GroupMessage],
    inline_dispatchers=[Kanata([FullMatch('百科'), RequireParam(name = 'tag')])]
    ))
async def bdbk(app: GraiaMiraiApplication, group: Group, member: Member, tag: MessageChain):
    tags = tag.asDisplay().strip().split(' ',1)
    
    bdurl = f'https://baike.baidu.com/item/{urllib.parse.quote(tags[0])}?force=1'
    async with aiohttp.request("GET", bdurl, headers = headers, allow_redirects = True) as r:
        if str(r.url) == 'https://baike.baidu.com/error.html':
            await app.sendGroupMessage(group, MessageChain.create([
                Plain('sorry,百科并没有相关信息')]))
            return
        reponse = await r.text()

    page = etree.HTML(reponse)
    if page.xpath('//div[@class="lemmaWgt-subLemmaListTitle"]//text()') != []:
        if len(tags) == 1:
            catalog = page.xpath('//div[@class="para" and @label-module="para"]/a/text()')
            await app.sendGroupMessage(group, MessageChain.create([
                Plain(f"请输入代号\ne.g:百科 {tags[0]} 1\n\n"),
                Plain('\n'.join(f"{n}.{w.replace(f'{tags[0]}：','')}" for n, w in enumerate(catalog)))
                ]))
            return
        use = int(tags[1]) - 1
        path = page.xpath('//div[@class="para" and @label-module="para"]/a/@href')[use]
        bdurl = r'https://baike.baidu.com' + path
        async with aiohttp.request("GET",bdurl,headers = headers) as r:
            reponse = await r.text()
        page = etree.HTML(reponse)

    for i in page.xpath('//div[@class="lemma-summary"]/div//sup'):
        i.getparent().remove(i)

    mem = page.xpath('//div[@class="lemma-summary"]/div//text()')
    mem = "".join(mem).replace('\n', '').replace('\xa0', '')

    mes = [Plain(f'{mem}\n' if mem else '没有简介desu\n'),
           Plain(bdurl.replace("?force=1",""))]
    
    if (img_url := page.xpath('//div[@class="summary-pic"]/a/img/@src')):
        mes.append(Image.fromNetworkAddress(img_url[0]))

    await app.sendGroupMessage(group, MessageChain.create(mes))

@channel.use(ListenerSchema(
    listening_events=[GroupMessage],
    inline_dispatchers=[Kanata([FullMatch('热点')])]
    ))
async def bdrd(app: GraiaMiraiApplication, group: Group, message: MessageChain, member: Member):
    url="http://top.baidu.com/buzz?b=1&fr=topindex"
    async with aiohttp.request("GET",url,headers = headers) as r:
        reponse = await r.text(encoding = 'gb2312')
    html = etree.HTML(reponse)
    get = html.xpath('//a[@class="list-title"]/text()')
    get = [f"{n+1}.{get[n]}" for n in range(len(get))]
    await app.sendGroupMessage(group, MessageChain.create([
        Plain('\n'.join(get[0:10]))]))
