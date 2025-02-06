from collections import defaultdict
import time


# Token Bucket Class
class TokenBucket:
    def __init__(self, max_tokens: int, refill_rate: float):
        """
        :param max_tokens: Maximum number of tokens the bucket can hold.
        :param refill_rate: Number of tokens added per second.
        """
        self.max_tokens = max_tokens
        self.tokens = max_tokens
        self.refill_rate = refill_rate
        self.last_refill_time = time.time()

    def consume(self, tokens: int = 1) -> bool:
        """
        Attempt to consume tokens from the bucket.
        :param tokens: Number of tokens to consume.
        :return: True if tokens were consumed, False otherwise.
        """
        # Refill tokens based on elapsed time
        current_time = time.time()
        elapsed_time = current_time - self.last_refill_time
        self.tokens = min(self.max_tokens, self.tokens + elapsed_time * self.refill_rate)
        self.last_refill_time = current_time

        # Check if there are enough tokens
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False