import time
from functools import wraps
import requests

def retry_with_exponential_backoff(max_retries=5, base_delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except requests.exceptions.RequestException as e:
                    if attempt == max_retries - 1:
                        raise e
                    delay = base_delay * (2 ** attempt)
                    time.sleep(delay)
            raise requests.exceptions.RequestException("Max retries exceeded")
        return wrapper
    return decorator