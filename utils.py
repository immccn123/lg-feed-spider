from hashlib import sha224

def calc_feed_hash(user_id: int, time: int, content: str):
    return str(user_id) + '|' + str(time) + '|' + sha224(content.encode('utf-8')).hexdigest()
