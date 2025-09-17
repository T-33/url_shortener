import string
import random

def generate_random_short_code(length: int = 7) -> str:
    """
    Generates a random alphanumeric short code of given length.
    """
    chars = string.digits + string.ascii_letters
    return "".join(random.choice(chars) for _ in range(length))