from dataclasses import dataclass
from environs import Env


@dataclass
class Config:
    bot_token: str
    db_name: str
    db_user: str
    db_password: str
    db_host: str
    db_port: str


def load_config() -> Config:
    env = Env()
    env.read_env()
    return Config(
        bot_token=env('BOT_TOKEN'),
        db_name=env('DB_NAME'),
        db_user=env('DB_NAME'),
        db_password=env('DB_PASSWORD'),
        db_host=env('DB_HOST'),
        db_port=env('DB_PORT'),
    )
