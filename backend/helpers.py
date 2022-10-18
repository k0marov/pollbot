from dataclasses import dataclass


@dataclass
class Response:
    """
    fields:
      code: int - code to return\n
      path: str - database path\n
      status: str - short description\n
      error_desc(opt): str - description of error\n
    """
    code: int
    path: str
    status: str
    error_desc: str = ""
