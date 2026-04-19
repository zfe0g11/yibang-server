import requests
import json
from typing import Optional
from ..properties.wechat_properties import WeChatProperties


class WeChatPayUtil:
    JSAPI = "https://api.mch.weixin.qq.com/v3/pay/transactions/jsapi"
    REFUNDS = "https://api.mch.weixin.qq.com/v3/refund/domestic/refunds"
    
    def __init__(self, wechat_properties: WeChatProperties):
        self.wechat_properties = wechat_properties
    
    def post(self, url: str, body: dict) -> Optional[dict]:
        try:
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Wechatpay-Serial": self.wechat_properties.mch_serial_no
            }
            response = requests.post(url, json=body, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
            return None