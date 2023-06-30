"""
零散的工具函数。
utils 的定义是无状态工具函数。
"""

from hashlib import sha224
import os


def calc_feed_hash(user_id: int, time: int, content: str):
    """根据犇犇信息计算哈希值。"""
    return (
        str(user_id)
        + "|"
        + str(time)
        + "|"
        + sha224(content.encode("utf-8")).hexdigest()
    )

def print_process(now,sumnum):
    """输出进度信息"""
    process_calculated = now*1. / sumnum
    print(f'{now:7} / {sumnum:7} {process_calculated*100:2.3f} %',end='')
    zdlen = os.get_terminal_size().columns-30
    print('[',end='')
    print('='*int(process_calculated*zdlen),end='')
    print('>',end='')
    print(' '*(zdlen-int(process_calculated*zdlen)),end='')
    print(']',end='\r')
