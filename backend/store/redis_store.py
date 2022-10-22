import json
import typing

import redis

from . import store


class RedisStore(store.Store):
    def __init__(self, client: redis.Redis):
        self._client = client

    def get(self, key: str) -> typing.Any:
        result = self._client.get(key)
        return json.loads(result) if result else None

    def set(self, key: str, value: typing.Any) -> None:
        self._client.set(key, json.dumps(value))