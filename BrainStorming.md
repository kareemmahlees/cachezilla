- get and set values
- support multiple cache eviction strategies

Example

```py

from cachezilla import CacheZilla

cache = CacheZilla(cache_evict="lru")

cache.set("name","kareem")
cache.set("age",14,5) # ttl

cache.get("name") # None if doesn't exist

```

- I am thinking to make the data source a linked list of CacheItem objects
- What happens when we set a new item ?
  it is added to the beginning of the data source keeping the new values with zero values
  in the rear (i.e at the head) and the oldest with higher frequency/recent in the front

- What happens when we get an item ?
  we return it to the user -> update the node's value -> re shuffle the linked list

item1 <-> item2 <-> item3 <-> item4

Example

```py

# we are moving item2
while (item2.last_used > item2.next.last_used):
    item2.next = item3.next
    item3.next.prev = item2
    item3.prev = item2.prev
    item1.next = item2.next
```

After a second thought, i think a doubly linked list will be overkill, there is no need to continuously advance the position of an item node every time we perform a `get`.
I think a better solution would be to use a singly linked list and when the time comes to evict we can traverse through the list and delete the highest node

right now i am not so sure about supporting multiple cache eviction strategies, we can see about that later after we settle on the basic functionality

It was a doubly linked list after all :)
