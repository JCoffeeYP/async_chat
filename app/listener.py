import asyncio
import logging
import os
import sys
from datetime import datetime

import aiofiles
from arg_parser import get_parser

logger = logging.getLogger(__file__)


def get_current_time():
    return f'[{datetime.now().strftime("%d.%m.%y %H:%M:%S:%f")[:-3]}]'


async def chat_listener(host: str, port: int, history: str):
    reader, writer = await asyncio.open_connection(host, port)

    async with aiofiles.open(os.path.expanduser(history), mode="a") as f:
        success_connection = f"{get_current_time()} Соединение установлено"
        await f.write(f"{success_connection}\n")
        while True:
            data = await reader.readline()
            msg = f"{get_current_time()} {data.decode()}"
            await f.write(msg)
            logger.debug(msg)
            print(f"{msg}\b")


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    logging.basicConfig(format="%(levelname):listener:%(message)s", level=logging.DEBUG)
    history = os.environ.get("HISTORY") or args.history
    host = os.environ.get("HOST") or args.host
    port = os.environ.get("PORT_LISTENER") or args.port_listener
    try:
        asyncio.run(chat_listener(host=host, port=port, history=history))
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
