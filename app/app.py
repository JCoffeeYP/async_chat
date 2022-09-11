import asyncio
from datetime import datetime

import aiofiles


def get_current_time():
    return f'[{datetime.now().strftime("%d.%m.%y %H:%M:%S:%f")[:-3]}]'


async def tcp_echo_client():
    reader, writer = await asyncio.open_connection('minechat.dvmn.org', 5000)

    async with aiofiles.open('minechat.txt', mode='a') as f:
        success_connection = f'{get_current_time()} Соединение установлено'
        await f.write(f'{success_connection}\n')
        while True:
            data = await reader.readline()
            msg = f'{get_current_time()} {data.decode()}'
            await f.write(msg)
            print(f'{msg}\b')

asyncio.run(tcp_echo_client())