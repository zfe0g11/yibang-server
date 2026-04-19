from pydantic import BaseModel


class AliOssProperties(BaseModel):
    endpoint: str
    access_key_id: str
    access_key_secret: str
    bucket_name: str