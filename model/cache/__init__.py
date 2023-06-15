from dogpile.cache import make_region, api

region = make_region().configure(
    "dogpile.cache.redis",
    expiration_time=3600,
    arguments = {
        "host": "redis",
        "port": 6379,
        "db": 1,
        "redis_expiration_time": 3600 
    }
)