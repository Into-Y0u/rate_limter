

# Global variables to store the token bucket state
from datetime import time
from typing import Dict, Tuple


token_buckets: Dict[str, Tuple[float, int]] = {}  # {client_ip: (last_refill_time, tokens)}

# Token bucket parameters
TOKEN_RATE = 1  # Tokens added per second
BUCKET_CAPACITY = 10  # Maximum tokens in the bucket

def refill_tokens(client_ip: str) -> int:
    """
    Refill the token bucket for a client based on the elapsed time.
    """
    current_time = time.time()
    last_refill_time, tokens = token_buckets.get(client_ip, (current_time, BUCKET_CAPACITY))

    # Calculate the time elapsed since the last refill
    elapsed_time = current_time - last_refill_time

    # Add tokens based on the elapsed time and token rate
    new_tokens = elapsed_time * TOKEN_RATE
    tokens = min(tokens + new_tokens, BUCKET_CAPACITY)

    # Update the last refill time and token count
    token_buckets[client_ip] = (current_time, tokens)

    return int(tokens)

def consume_token(client_ip: str) -> bool:
    """
    Consume a token from the bucket for a client.
    Returns True if a token is available, False otherwise.
    """
    tokens = refill_tokens(client_ip)

    if tokens >= 1:
        token_buckets[client_ip] = (token_buckets[client_ip][0], tokens - 1)
        return True
    return False
