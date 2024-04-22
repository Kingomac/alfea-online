import redis

redis_db = redis.Redis(host='als-redis', port=6379, db=0)
