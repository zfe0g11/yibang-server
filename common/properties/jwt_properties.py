from pydantic import BaseModel


class JwtProperties(BaseModel):
    admin_secret_key: str
    admin_ttl: int
    admin_token_name: str
    
    user_secret_key: str
    user_ttl: int
    user_token_name: str