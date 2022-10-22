import abc
import json
from abc import abstractmethod
from helpers import Response
from typing import Any


class Database(abc.ABC):
    @abstractmethod
    def get(self):
        raise NotImplementedError("Abstract method 'Database.get()' was not implemented/")

    @abstractmethod
    def push(self, data):
        raise NotImplementedError("Abstract method 'Database.push()' was not implemented/")


class JsonDatabase(Database):
    def __init__(self, path: str):
        self.__path = path
        self.__info: dict = {}
        self.__data = ""

    def get(self):
        try:
            with open(self.__path, "r") as file:
                self.__data = json.load(file)
            return Response(200, self.__path, "success", self.__data)

        except BaseException as e:
            return Response(404, self.__path, "error", str(e))

    def push(self, data):
        try:
            with open(self.__path, "w") as file:
                file.write(json.dumps({"Data": data}))
            return Response(200, self.__path, "success", self.__data)

        except BaseException as e:
            return Response(404, self.__path, "error", str(e))
