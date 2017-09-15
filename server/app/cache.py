"""redis cache."""
import redis

KVSTORE = redis.StrictRedis(host='localhost', port=6379, db=2)
