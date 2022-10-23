import abc

import typing


class Store(abc.ABC):
    @abc.abstractmethod
    def get(self, key: str) -> typing.Any: pass
    @abc.abstractmethod
    def set(self, key: str, value: typing.Any) -> None: pass