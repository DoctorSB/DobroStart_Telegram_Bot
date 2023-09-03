from dataclasses import dataclass
from typing import Optional
from environs import Env
import psycopg2 as pg


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str
    port: int = 5432

    def get_connect(self):
        return pg.connect(dbname=self.database, user=self.user, password=self.password, host=self.host, port=self.port)

    def print_info(self):
        print(f'dbname = {self.dbname}\n'
              f'user = {self.user}\n'
              f'passwd = {self.password}\n'
              f'host = {self.host}\n'
              f'port = {self.port}\n'
              f'table = {self.table}\n')

    @staticmethod
    def from_env(env: Env):
        """
        Creates the DbConfig object from environment variables.
        """
        host = env.str("DB_HOST")
        password = env.str("POSTGRES_PASSWORD")
        user = env.str("POSTGRES_USER")
        database = env.str("POSTGRES_DB")
        port = env.int("DB_PORT")
        return DbConfig(
            host=host, password=password, user=user, database=database, port=port
        )


@ dataclass
class TgBot:
    """
    Creates the TgBot object from environment variables.
    """

    token: str
    admin_ids: list[int]
    use_redis: bool
    payment_token: str = None

    @ staticmethod
    def from_env(env: Env):

        payment_token = env.str("PAYMENTS_TOKEN")
        token = env.str("BOT_TOKEN")
        admin_ids = list(map(int, env.list("ADMINS")))
        use_redis = env.bool("USE_REDIS")
        return TgBot(token=token, admin_ids=admin_ids, use_redis=use_redis, payment_token=payment_token)


@ dataclass
class RedisConfig:
    redis_pass: Optional[str]
    redis_port: Optional[int]
    redis_host: Optional[str]

    def dsn(self) -> str:
        """
        Constructs and returns a Redis DSN (Data Source Name) for this database configuration.
        """
        if self.redis_pass:
            return f"redis://:{self.redis_pass}@{self.redis_host}:{self.redis_port}/0"
        else:
            return f"redis://{self.redis_host}:{self.redis_port}/0"

    @ staticmethod
    def from_env(env: Env):
        """
        Creates the RedisConfig object from environment variables.
        """
        redis_pass = env.str("REDIS_PASSWORD")
        redis_port = env.int("REDIS_PORT")
        redis_host = env.str("REDIS_HOST")

        return RedisConfig(
            redis_pass=redis_pass, redis_port=redis_port, redis_host=redis_host
        )


@ dataclass
class Miscellaneous:
    other_params: str = None


@ dataclass
class Config:
    tg_bot: TgBot
    misc: Miscellaneous
    db: Optional[DbConfig] = None
    redis: Optional[RedisConfig] = None


def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot.from_env(env),
        db=DbConfig.from_env(env),
        # redis=RedisConfig.from_env(env),
        misc=Miscellaneous(),
    )
