class ContextCache:
    def __init__(self):
        self.cache = {}

    def add(self, cache_uuid: str, item: dict):
        self.cache[cache_uuid] = item

    def remove(self, cache_uuid: str):
        self.cache.pop(cache_uuid, None)

    def get(self, cache_uuid: str):
        return self.cache.get(cache_uuid, None)
