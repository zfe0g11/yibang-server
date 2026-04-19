import json
from datetime import datetime, date, time
from typing import Any, Dict


class JacksonObjectMapper:
    DEFAULT_DATE_FORMAT = "yyyy-MM-dd"
    DEFAULT_DATE_TIME_FORMAT = "yyyy-MM-dd HH:mm"
    DEFAULT_TIME_FORMAT = "HH:mm:ss"
    
    @staticmethod
    def serialize(obj: Any) -> str:
        return json.dumps(obj, default=JacksonObjectMapper._serialize_datetime)
    
    @staticmethod
    def deserialize(json_str: str, cls: type = None) -> Any:
        return json.loads(json_str, object_hook=lambda d: JacksonObjectMapper._deserialize_datetime(d, cls))
    
    @staticmethod
    def _serialize_datetime(obj: Any) -> str:
        if isinstance(obj, datetime):
            return obj.strftime(JacksonObjectMapper.DEFAULT_DATE_TIME_FORMAT)
        elif isinstance(obj, date):
            return obj.strftime(JacksonObjectMapper.DEFAULT_DATE_FORMAT)
        elif isinstance(obj, time):
            return obj.strftime(JacksonObjectMapper.DEFAULT_TIME_FORMAT)
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")
    
    @staticmethod
    def _deserialize_datetime(d: Dict[str, Any], cls: type = None) -> Any:
        if cls:
            # 如果指定了类，尝试直接转换
            return cls(**d)
        return d