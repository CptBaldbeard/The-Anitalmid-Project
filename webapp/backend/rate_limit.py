"""Simple in-memory rate limiter — no external dependencies.

Keys hit timestamps per window and rejects once the limit is exceeded.
State is lost on restart (acceptable for a single-instance free-tier deploy).
"""
import time
from collections import defaultdict, deque


class RateLimiter:
    def __init__(self) -> None:
        self._hits: dict[str, deque] = defaultdict(deque)

    def allow(self, key: str, limit: int, window: float) -> bool:
        now = time.monotonic()
        dq = self._hits[key]
        while dq and dq[0] <= now - window:
            dq.popleft()
        if len(dq) >= limit:
            return False
        dq.append(now)
        return True


# Per-IP: 10 analyses/hour — blocks scripted/abusive hammering.
ip_limiter = RateLimiter()
# Per-user: 25 analyses/day — generous for a portfolio demo.
user_limiter = RateLimiter()
