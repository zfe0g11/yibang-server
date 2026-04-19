import oss2
from typing import Optional

# 阿里云 OSS 配置

class AliOssUtil:
    def __init__(self, endpoint: str = ALI_OSS_ENDPOINT, access_key_id: str = ALI_OSS_ACCESS_KEY_ID, 
                 access_key_secret: str = ALI_OSS_ACCESS_KEY_SECRET, bucket_name: str = ALI_OSS_BUCKET_NAME):
        self.endpoint = endpoint
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.bucket_name = bucket_name
        self.auth = oss2.Auth(access_key_id, access_key_secret)
        self.bucket = oss2.Bucket(self.auth, endpoint, bucket_name)
    
    def upload(self, bytes_data: bytes, object_name: str) -> Optional[str]:
        try:
            self.bucket.put_object(object_name, bytes_data)
            # 构造文件访问路径
            url = f"https://{self.bucket_name}.{self.endpoint}/{object_name}"
            print(f"文件上传到:{url}")
            return url
        except oss2.exceptions.OssError as e:
            print(f"OSS错误: {e}")
            return None
        except Exception as e:
            print(f"上传失败: {e}")
            return None


# 创建阿里云 OSS 工具实例
ali_oss_util = AliOssUtil()