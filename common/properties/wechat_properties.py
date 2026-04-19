from pydantic import BaseModel


class WeChatProperties(BaseModel):
    appid: str
    secret: str
    mchid: str
    mch_serial_no: str
    private_key_path: str
    api_v3_key: str
    wechat_pay_cert_path: str
    notify_url: str
    refund_notify_url: str