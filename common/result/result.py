from typing import Generic, TypeVar, Optional

T = TypeVar('T')


class Result(Generic[T]):
    def __init__(self, code: int, msg: str = "", data: Optional[T] = None):
        self.code = code
        self.msg = msg
        self.data = data
    
    @staticmethod
    def success(data: Optional[T] = None) -> 'Result[T]':
        return Result(1, data=data)
    
    @staticmethod
    def error(msg: str) -> 'Result[None]':
        return Result(0, msg=msg)
    
    def to_dict(self) -> dict:
        return {
            "code": self.code,
            "msg": self.msg,
            "data": self.data
        }