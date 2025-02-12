# Rate Limiter Manager
from collections import defaultdict
from token_bucket import TokenBucket


class RaterLimiterTypes:
    bucket = None
    def __init__(self, bucket_name: str, max_tokens: int, refill_rate: float):
        self.bucket_name = bucket_name
        self.bucket = TokenBucket(max_tokens, refill_rate)

    def get_main_bucket(self):
        return self.bucket
        
class GlobalRateLimiter(RaterLimiterTypes):
    bucket_name = "global"
    max_tokens = 2 
    refill_rate = 1
    def __init__(self):
        super().__init__(self.bucket_name, self.max_tokens, self.refill_rate)      

class IpRateLimiter(RaterLimiterTypes):
    bucket_name = "ip"
    max_tokens = 2 
    refill_rate = 0.001
    def __init__(self):
        super().__init__(self.bucket_name, self.max_tokens, self.refill_rate)   




    