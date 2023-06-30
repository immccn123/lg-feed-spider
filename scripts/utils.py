"""
零散的工具函数。
utils 的定义是无状态工具函数。
"""

from hashlib import sha224


def calc_feed_hash(user_id: int, time: int, content: str):
    """根据犇犇信息计算哈希值。"""
    return (
        str(user_id)
        + "|"
        + str(time)
        + "|"
        + sha224(content.encode("utf-8")).hexdigest()
    )
