import string
import random
import re

def generate_random_short_code(length: int = 7) -> str:
    """
    Generates a random alphanumeric short code of given length.
    """
    if not isinstance(length, int):
        raise ValueError(f'Random short code length must be of type int. Provided type: {type(length)}')

    if length <= 0:
        raise ValueError(f'Random short code length must be greater than 0. Provided length: {length}')

    chars = string.digits + string.ascii_letters
    return "".join(random.choice(chars) for _ in range(length))

def is_valid_short_code_name(short_code: str) -> bool:
    """
    Checks if provided short_code doesn't contain characters with special url meaning.
    """
    return re.sub(r'[_-]', '', short_code).isalnum()