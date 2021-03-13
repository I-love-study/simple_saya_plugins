import asyncio
from graia.saya import Saya
from graia.broadcast import Broadcast
from graia.saya.builtins.broadcast import BroadcastBehaviour
from graia.application import GraiaMiraiApplication, Session

from util import get_module_in_dir
import yaml
import logging
logging.basicConfig(format="[%(asctime)s][%(levelname)s]: %(message)s", level=logging.INFO)

loop = asyncio.get_event_loop()
bcc = Broadcast(loop=loop)
saya = Saya(bcc)
saya.install_behaviours(BroadcastBehaviour(bcc))

with open('configs.yml', encoding='UTF-8') as f:
    configs = yaml.safe_load(f)

app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host=configs["miraiHost"],
        authKey=configs["authKey"],
        account=configs['account'],
        websocket=True
    )
)

load_module = [module for folder in configs['load_folder'] 
    for module in get_module_in_dir(folder)]

with saya.module_context():
    for module in load_module:
        saya.require(module)


app.launch_blocking()

try:
    loop.run_forever()
except KeyboardInterrupt:
    exit()