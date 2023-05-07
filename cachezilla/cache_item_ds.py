from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional


@dataclass
class CacheItem:

    """The DataStructure responsible for storing the item info."""

    key: Any
    value: Any
    ttl: datetime | None
    last_used: Optional[datetime] = None
    next: Optional["CacheItem"] = None
    prev: Optional["CacheItem"] = None
