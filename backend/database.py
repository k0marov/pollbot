import json
from abc import abstractmethod
from helpers import Response


class Database:
    @abstractmethod
    def get(self):
        raise NotImplementedError("Abstract method 'Database.get()' was not implemented/")

    @abstractmethod
    def push(self, data):
        raise NotImplementedError("Abstract method 'Database.push()' was not implemented/")


class JsonDatabase(Database):
    def __init__(self, path: str):
        self.info: dict = {}
        self.__path = path

    def get(self):
        try:
            with open(self.__path, "r") as file:
                self.info = json.load(file)
            return self.info

        except BaseException as e:
            return Response(404, self.__path, "error", str(e))

    def push(self, data):
        with open(self.__path, "w") as file:
            file.write(json.dumps(data))