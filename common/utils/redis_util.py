# app/utils/redis_util.py
from numpy import tri
import redis
import json
import os
from dotenv import load_dotenv

load_dotenv()

class RedisUtil:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = redis.Redis(
                host=os.getenv("REDIS_HOST", "localhost"),
                port=int(os.getenv("REDIS_PORT", 6379)),
                db=int(os.getenv("REDIS_DB", 0)),
                password=os.getenv("REDIS_PASSWORD", None),
                decode_responses=True
            )
        return cls._instance
    
    def setex(self, key, expire, value):
        # 处理 key 中的引号
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        self.client.setex(key, expire, value)
    
    def get(self, key):
        # 处理 key 中的引号
        value = self.client.get(key)
        if value:
            try:
                return json.loads(value)
            except:
                return value
        return None
    
    def incr(self, key):
        # 处理 key 中的引号
        key = str(key).replace("'", "").replace('"', '')
        return self.client.incr(key)
    
    def delete(self, key):
        # 处理 key 中的引号
        key = str(key).replace("'", "").replace('"', '')
        return self.client.delete(key)

redis_util = RedisUtil()