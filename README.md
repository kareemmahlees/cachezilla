# _**CacheZilla**_

CacheZilla is a lightweight caching system ( source code is approximately only one file ) that supports `key,value` based storage and `ttl` ( time to live ).

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white">

## Examples

```py
from cachezilla import CacheZilla

cache = CacheZilla() # optional: max_size

cache.set("name","kareem")
cache.set("age",20,ttl=5)

cache.get("name") # >> kareem
```
