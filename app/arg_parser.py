import argparse


def get_parser():
    parser = argparse.ArgumentParser(
        description="Chat developed on netchat(nc) " "and Python asyncio technologies"
    )
    parser.add_argument(
        "--history",
        type=str,
        default="~/chat.history",
        help="Path of history file (default: ~/chat.history)",
    )
    parser.add_argument(
        "--host",
        type=str,
        default="minechat.dvmn.org",
        help="host address",
    )
    parser.add_argument(
        "--port_listener",
        type=int,
        default=5000,
        help="listener port number",
    )
    parser.add_argument(
        "--port_sender",
        type=int,
        default=5050,
        help="sender port number",
    )
    parser.add_argument(
        "--token",
        type=str,
        default="",
        help="chat token",
    )

    return parser
