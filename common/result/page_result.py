from typing import Generic, TypeVar, List

T = TypeVar('T')


class PageResult(Generic[T]):
    def __init__(self, total: int, records: List[T]):
        self.total = total
        self.records = records
    
    def to_dict(self) -> dict:
        return {
            "total": self.total,
            "records": self.records
        }