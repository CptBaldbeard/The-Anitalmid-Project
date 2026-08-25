"""Deterministic salary-range parsing and overlap matching (no LLM).

Role ``salary_range`` strings look like ``"$65K-$90K (mid), $90K-$120K (senior)"``.
We extract the numeric figures and expose the full earning span as ``(min_k, max_k)``,
then test whether that span overlaps a user's preferred salary range.
"""
import re

# Matches the "$NNK" figures used throughout the catalog (e.g. "$65K", "$120K",
# "$90K"). The "+" in "$120K+" is deliberately ignored.
_K_RE = re.compile(r"\$(\d{2,3})K", re.IGNORECASE)


def parse_salary_range(salary_str: str) -> tuple[int, int] | None:
    """Return the (min_k, max_k) earning span for a role, or None if unparseable."""
    if not salary_str:
        return None
    nums = [int(m) for m in _K_RE.findall(salary_str)]
    if not nums:
        return None
    return min(nums), max(nums)


def salary_fits(role_salary: str, user_min: int | None, user_max: int | None) -> bool | None:
    """Return True when a role's salary span overlaps the user's preferred range.

    Returns None when there's no user range, or the role's salary is unparseable.
    """
    if user_min is None or user_max is None:
        return None
    if user_min > user_max:
        user_min, user_max = user_max, user_min
    span = parse_salary_range(role_salary)
    if span is None:
        return None
    role_min, role_max = span
    return role_max >= user_min and role_min <= user_max
