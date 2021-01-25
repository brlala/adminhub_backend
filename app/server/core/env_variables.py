from decouple import config


class LocalConfig:
    JWT_SECRET_KEY: str = config('JWT_SECRET_KEY')
    JWT_ALGORITHM: str = config('JWT_ALGORITHM')
    DATABASE_NAME: str = config('DATABASE_NAME')
    MONGODB_URL: str = config('MONGODB_URL')
    TIMEZONE: str = config('TIMEZONE')
    CLOUD_ACCESS_KEY: str = config('CLOUD_ACCESS_KEY')
    CLOUD_SECRET_ACCESS_KEY: str = config('CLOUD_SECRET_ACCESS_KEY')
    CLOUD_BUCKET_URL: str = config('CLOUD_BUCKET_URL')
    CLOUD_BUCKET_NAME: str = config('CLOUD_BUCKET_NAME')
    CLOUD_PROVIDER: str = config('CLOUD_PROVIDER')
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = config('JWT_ACCESS_TOKEN_EXPIRE_MINUTES', cast=int)
    ALLOWED_HOSTS: list[str] = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])


local_config = LocalConfig()
