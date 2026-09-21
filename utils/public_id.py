"""Module for generating unique public IDs for farm entities.

This module provides a function to create a random, human-readable,
and unique public ID for new SmartFarmOS instances.
"""
import secrets

ALPHABET: str = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"

def generate_public_farm_id(length: int = 10) -> str:
    """Generates a unique, human-readable public ID for a farm.

    The ID follows a pattern like 'SFO-XXXX-YY', where X and Y are random
    characters from a predefined alphabet. The default length for the random
    parts totals 10 characters.

    Args:
        length (int): The total length of the random character parts (default is 10).
                      Note: The 'SFO-' prefix and hyphens are added separately.

    Returns:
        str: A unique public ID string, e.g., 'SFO-ABCD-EF'.
    """

    first_part: str = "".join(
        secrets.choice(ALPHABET)
        for _ in range(4)
    )

    second_part: str = "".join(
        secrets.choice(ALPHABET)
        for _ in range(2)
    )

    return f"SFO-{first_part}-{second_part}"
