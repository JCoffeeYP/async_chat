import asyncio
import json
import logging
import os
import sys
from asyncio import StreamReader, StreamWriter

from arg_parser import get_parser

logger = logging.getLogger(__file__)


async def read_and_print_line(reader: StreamReader) -> None:
    data = await reader.readline()
    decoded_data = f"{data.decode()}\b"
    logger.debug(decoded_data)
    print(decoded_data)


async def check_token(reader: StreamReader) -> bool:
    data = await reader.readline()
    json_data = json.loads(data)
    if json_data:
        decoded_data = f"{data.decode()}\b"
        logger.debug(decoded_data)
        print(decoded_data)

        return True

    wrong_token_msg = "Неизвестный токен. Проверьте его или зарегистрируйте заново."
    logger.debug(wrong_token_msg)
    print(wrong_token_msg)

    return False


async def user_authorization(reader: StreamReader, writer: StreamWriter) -> None:
    await read_and_print_line(reader)

    token = f"{input()}\n"
    writer.write(token.encode())
    await writer.drain()
    logger.debug(f"{token}\b")

    if not await check_token(reader):
        await read_and_print_line(reader)

        username = f"{input()}\n"
        writer.write(username.encode())
        await writer.drain()
        logger.debug(f"{username}\b")

        await read_and_print_line(reader)


async def chat_sender(host: str, port: int):
    reader, writer = await asyncio.open_connection(host, port)
    await user_authorization(reader, writer)

    while True:
        await read_and_print_line(reader)
        msg = f"{input()}\n\n"
        writer.write(msg.encode())
        await writer.drain()


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    logging.basicConfig(format="%(levelname)s:sender:%(message)s", level=logging.DEBUG)
    history = os.environ.get("HISTORY") or args.history
    host = os.environ.get("HOST") or args.host
    port = os.environ.get("PORT_SENDER") or args.port_sender

    try:
        asyncio.run(chat_sender(host=host, port=port))
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
