import redis
from django.conf import settings


class RedisUtil:
    redis_cli = None

    @staticmethod
    def get_redis_client():
        if not RedisUtil.redis_cli:
            pool = redis.ConnectionPool(
                host=settings.REDIS_CACHE_HOST,
                port=settings.REDIS_CACHE_PORT,
                db=settings.REDIS_CACHE_DB,
                decode_responses=True
            )
            RedisUtil.redis_cli = redis.Redis(connection_pool=pool)
        return RedisUtil.redis_cli
