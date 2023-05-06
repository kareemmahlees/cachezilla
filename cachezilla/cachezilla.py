from datetime import datetime
from typing import Any

from .cache_item_ds import CacheItem


class CacheZilla:
    """Entry point of the system."""

    def __init__(
        self,
        max_size: int | None = None,
    ) -> None:
        self.head: CacheItem | None = None
        self.tail: CacheItem | None = None
        self.max_size = max_size
        self.size = 0

    def set(self, key: Any, value: Any, ttl: int | None = None) -> int:
        """Add the item to the linked list.
        Args:
            key (Any): item key
            value (Any): item value
            ttl (int | None, optional): time after which the item will expire
            . Defaults to None.

        Returns:
            int: number of items inserted

        """
        item = CacheItem(key, value, ttl)

        if self.max_size and self.size == self.max_size:
            self.__evict()

        # the first insertion
        if self.head is None or self.tail is None:
            self.head = self.tail = item
        else:
            self.__insert_item(item)
        self.size += 1
        return 1

    def get(self, key: Any) -> Any:
        """Get the item value.

        Args:
            key (Any): item key

        Returns:
            Any: the item value
        """
        current = self.head
        while current is not None:
            if current.key == key:
                break
            current = current.next
        else:
            return None
        current.last_used = datetime.now()
        return current.value

    def __remove_item(self, item: CacheItem) -> None:
        # guard clause for the tail
        if item.next is None:
            item.prev.next = None
            self.tail = item.prev
            item.prev = None
            return
        # guard clause for the head
        if item.prev is None:
            item.next.prev = None
            self.head = item.next
            item.next = None
            return
        item.prev.next = item.next
        item.next.prev = item.prev
        item.next = item.prev = None

    def __evict(self) -> None:
        least_recently_used: CacheItem | None = self.head
        current = self.head

        # get the lru item
        while current is not None:
            if current.last_used is None:
                least_recently_used = current
                current = current.next
                continue
            if (
                least_recently_used.last_used is not None
                and current.last_used < least_recently_used.last_used
            ):  # type: ignore
                least_recently_used = current
                current = current.next
                continue
            current = current.next

        # remove the lru item
        self.__remove_item(least_recently_used)  # type:ignore
        self.size -= 1

    def __insert_item(self, item: CacheItem) -> None:
        next_node = self.head
        item.next = next_node
        next_node.prev = item
        self.head = item
