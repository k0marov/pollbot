from dataclasses import dataclass
from typing import Any


@dataclass
class Response:
    """
    fields:
      code: int - code to return\n
      path: str - database path\n
      status: str - short description\n
      response(opt): str - response text\n
    """
    code: int
    path: str
    status: str
    response: Any = ""


