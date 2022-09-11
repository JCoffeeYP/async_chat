import asyncio
import os
import sys
from datetime import datetime
from pathlib import Path

import aiofiles

from arg_parser import get_parser


def get_current_time():
    return f'[{datetime.now().strftime("%d.%m.%y %H:%M:%S:%f")[:-3]}]'


async def chat_listener(host: str, port: int, history: str):
    reader, writer = await asyncio.open_connection(host, port)

    async with aiofiles.open(os.path.expanduser(history), mode='a') as f:
        success_connection = f'{get_current_time()} Соединение установлено'
        await f.write(f'{success_connection}\n')
        while True:
            data = await reader.readline()
            msg = f'{get_current_time()} {data.decode()}'
            await f.write(msg)
            print(f'{msg}\b')


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    history = os.environ.get("HISTORY") or args.history
    host = os.environ.get("HOST") or args.host
    port = os.environ.get("PORT") or args.port
    try:
        asyncio.run(chat_listener(host=host, port=port, history=history))
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
