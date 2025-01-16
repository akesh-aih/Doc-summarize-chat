import redis
from loguru import logger

class RedisCache:
    def __init__(self, host='localhost', port=6379, db=0):
        """Initialize the Redis client."""
        self.redis_client = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)
        logger.debug(f"Connected to Redis at {host}:{port}, DB {db}")
    
    def check_cached_response(self, query):
        """Check if the query is already cached in Redis."""
        cached_response = self.redis_client.get(query)
        if cached_response:
            logger.debug("Cache hit! Returning cached response.")
        else:
            logger.debug("Cache miss. Query not found in cache.")
        return cached_response

    def cache_response(self, query, response):
        """Cache the response for a given query in Redis."""
        try:
            self.redis_client.set(query, response)
            logger.debug(f"Cached response for query: {query}")
        except Exception as e:
            logger.error(f"Error caching response: {e}")
    
    def delete_cached_response(self, query):
        """Delete a cached response for a given query in Redis."""
        try:
            self.redis_client.delete(query)
            logger.debug(f"Deleted cached response for query: {query}")
        except Exception as e:
            logger.error(f"Error deleting cached response: {e}")

    def clear_all_cache(self):
        """Clear all cached responses in Redis."""
        try:
            self.redis_client.flushdb()
            logger.debug("All cached responses cleared.")
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
