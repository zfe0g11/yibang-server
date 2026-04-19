import jwt
from datetime import datetime, timedelta

class JwtUtil:
    @staticmethod
    def create_jwt(secret_key: str, ttl_millis: int, payload: dict) -> str:
        """创建 JWT 令牌"""
        expiration = datetime.utcnow() + timedelta(milliseconds=ttl_millis)
        payload["exp"] = expiration
        return jwt.encode(payload, secret_key, algorithm="HS256")
    
    @staticmethod
    def verify_jwt(token: str, secret_key: str) -> bool:
        """验证 JWT 令牌"""
        try:
            jwt.decode(token, secret_key, algorithms=["HS256"])
            return True
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False
    
    @staticmethod
    def decode_jwt(token: str, secret_key: str) -> dict:
        """解码 JWT 令牌"""
        return jwt.decode(token, secret_key, algorithms=["HS256"])