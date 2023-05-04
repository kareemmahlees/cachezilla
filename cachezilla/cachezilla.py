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
        queue_item = CacheItem(key, value, ttl)

        if self.max_size and self.size == self.max_size:
            current_highest = self.head
            current = self.head
            # get the most recent cache item
            while current is not None:
                if (
                    current.last_used is not None
                    and current_highest.last_used is not None
                    and current.last_used
                    > current_highest.last_used  # type:ignore # noqa
                ):
                    current_highest = current
                current = current.next

            # true if all the items have not been used
            if current_highest.last_used is None:
                prev_node = self.tail.prev
                self.tail.prev = None
                self.tail = prev_node
                return 1

            # remove the most recently used item
            self.__remove_item(current_highest)  # type:ignore
            self.size -= 1

        if self.head is None or self.tail is None:
            self.head = self.tail = queue_item
        else:
            next_node = self.head
            queue_item.next = next_node
            next_node.prev = queue_item
            self.head = queue_item
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
        while current.next is not None:
            if current.key == key:
                break
            current = current.next
        current.last_used = datetime.now()
        return current.value

    def __remove_item(self, item: CacheItem) -> None:
        item.prev.next = item.next
        item.next.prev = item.prev
        item.next = item.prev = None
