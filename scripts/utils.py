"""
零散的工具函数。
utils 的定义是无状态工具函数。
"""

import os
import sys
import json
import time
from hashlib import sha224

import requests

from tools.logger import HandleLog

logger = HandleLog()


def calc_feed_hash(user_id: int, time: int, content: str):
    """根据犇犇信息计算哈希值。"""
    return (
        str(user_id)
        + "|"
        + str(time)
        + "|"
        + sha224(content.encode("utf-8")).hexdigest()
    )


def print_process(now: int, sumnum: int):
    """输出进度信息"""
    process_calculated = now * 1.0 / sumnum
    print(f"{now:7} / {sumnum:7} {process_calculated*100:2.3f} %", end="")
    zdlen = os.get_terminal_size().columns - 30
    print("[", end="")
    print("=" * int(process_calculated * zdlen), end="")
    print(">", end="")
    print(" " * (zdlen - int(process_calculated * zdlen)), end="")
    print("]", end="\r")


def grab(page: int) -> dict:
    """爬取第x页犇犇的函数"""
    assert page >= 1

    status_code = None

    for i in range(5):
        try:
            result_get = requests.get(
                "https://www.luogu.com.cn/api/feed/list?page=" + str(page),
                headers={
                    "user-agent":
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/125.0.0.0 Safari/537.36"
                },
                timeout=10,
            )
            status_code = result_get.status_code
            assert result_get.status_code == 200
            return json.loads(
                result_get.content.decode("utf-8", errors="replace").replace("\x00", "\uFFFD")
            )["feeds"]["result"]
        except TimeoutError:
            logger.error("Timed out while getting feeds. Retrying...")
        except AssertionError:
            logger.error(f"Luogu returned a response with code {status_code}, retrying...")
            time.sleep(i + 1)

    logger.critical("Retried 5 times, aborted.")
    sys.exit(1)
