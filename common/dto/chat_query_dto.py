from dataclasses import dataclass
from typing import Optional, List

@dataclass
class ChatQueryDTO:
    session_id: Optional[str] = None
    query: Optional[str] = None
    history: Optional[List[dict]] = None