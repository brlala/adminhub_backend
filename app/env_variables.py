from decouple import config


class LocalConfig:
    SECRET_KEY: str = config('SECRET_KEY')
    ALGORITHM: str = config('ALGORITHM')
    DATABASE_NAME: str = config('DATABASE_NAME')
    MONGODB_URL: str = config('MONGODB_URL')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = config('ACCESS_TOKEN_EXPIRE_MINUTES', cast=int)
    ALLOWED_HOSTS: list[str] = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])


local_config = LocalConfig()
