import asyncio
import os
import sys
from asyncio import StreamReader, StreamWriter

from arg_parser import get_parser


async def read_and_print_line(reader: StreamReader) -> None:
    data = await reader.readline()
    print(f"{data.decode()}\b")


async def user_authorization(reader: StreamReader, writer: StreamWriter, token: str = "") -> None:
    await read_and_print_line(reader)
    if token:
        print(f"the current session will use the preset token: {token}")
        writer.write(f"{token}\n".encode())
        await writer.drain()
    else:
        writer.write("\n".encode())
        await read_and_print_line(reader)
        username = f"{input()}\n"
        writer.write(username.encode())
        await writer.drain()
    await read_and_print_line(reader)


async def chat_sender(host: str, port: int, token: str):
    reader, writer = await asyncio.open_connection(host, port)
    await user_authorization(reader, writer, token)

    while True:
        await read_and_print_line(reader)
        msg = f"{input()}\n\n"
        writer.write(msg.encode())
        await writer.drain()


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    history = os.environ.get("HISTORY") or args.history
    host = os.environ.get("HOST") or args.host
    port = os.environ.get("PORT_SENDER") or args.port_sender
    token = os.environ.get("TOKEN") or args.token
    try:
        asyncio.run(chat_sender(host=host, port=port, token=token))
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
