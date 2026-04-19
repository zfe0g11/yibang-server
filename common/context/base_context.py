import threading
from typing import Optional


class BaseContext:
    _thread_local = threading.local()
    
    @staticmethod
    def set_current_id(id: int) -> None:
        setattr(BaseContext._thread_local, "current_id", id)
    
    @staticmethod
    def get_current_id() -> Optional[int]:
        return getattr(BaseContext._thread_local, "current_id", None)
    
    @staticmethod
    def remove_current_id() -> None:
        if hasattr(BaseContext._thread_local, "current_id"):
            delattr(BaseContext._thread_local, "current_id")