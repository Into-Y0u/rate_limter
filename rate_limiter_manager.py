# Rate Limiter Manager
from collections import defaultdict
from token_bucket import TokenBucket


class RateLimiter:
    def __init__(self):
        self.buckets = defaultdict(lambda: {})

    def get_bucket(self, bucket_type: str, key: str, max_tokens: int, refill_rate: float) -> TokenBucket:
        """
        Get or create a token bucket for a specific type and key.
        :param bucket_type: Type of bucket (e.g., "user", "api", "ip").
        :param key: Unique identifier for the bucket (e.g., user ID, IP address).
        :param max_tokens: Maximum tokens for the bucket.
        :param refill_rate: Refill rate for the bucket.
        :return: TokenBucket instance.
        """
        if key not in self.buckets[bucket_type]:
            self.buckets[bucket_type][key] = TokenBucket(max_tokens, refill_rate)
        return self.buckets[bucket_type][key]

    def check_limit(self, bucket_type: str, key: str, max_tokens: int, refill_rate: float) -> bool:
        """
        Check if a request is allowed based on the token bucket.
        :param bucket_type: Type of bucket.
        :param key: Unique identifier for the bucket.
        :param max_tokens: Maximum tokens for the bucket.
        :param refill_rate: Refill rate for the bucket.
        :return: True if allowed, False otherwise.
        """
        bucket = self.get_bucket(bucket_type, key, max_tokens, refill_rate)
        return bucket.consume()
