import dataclasses
import os

import typing
import dotenv


@dataclasses.dataclass
class Config:
    bot_token: str
    admin_pass: str

def load_config() -> Config:
    dotenv.load_dotenv()
    TOKEN_KEY = "ANONYMOUS_POLL_BOT_TOKEN"
    ADMIN_PASS_KEY = "ANONYMOUS_POLL_ADMIN_PASS"
    return Config(bot_token=_load_env(TOKEN_KEY), admin_pass=_load_env(ADMIN_PASS_KEY))

def _load_env(key: str) -> str:
    val = os.environ.get(key)
    if val is None:
        print(f"Please fill in the {key} environment variable.")
        exit(1)
    return val
