"""Utility Functions for project-wide use"""

from multiprocessing.sharedctypes import Value
import random
import string


def generate_random_code(length: int = 5) -> str:
    """Generate a random code of digits of a given length"""
    start = 10 ** length
    end = 10 ** (length + 1) - 1
    return str(random.randint(start, end))


def generate_random_string(length: int = 5, use_upper=True, use_lower=True,
                           use_digit=True, use_symbols=True) -> str:
    """Generate a random string of letters of a given length"""
    chars = ""
    if use_digit:
        chars += string.digits
    if use_lower:
        chars += string.ascii_lowercase
    if use_upper:
        chars += string.ascii_uppercase
    if use_symbols:
        chars += string.punctuation
    if not chars:
        raise ValueError
    return ''.join(random.choices(chars, k=length))


def persian_digits_to_english(string):
    return (string
            .replace('۰', '0').replace('۱', '1').replace('۲', '2')
            .replace('۳', '3').replace('۴', '4').replace('۵', '5')
            .replace('۶', '6').replace('۷', '7').replace('۸', '8')
            .replace('۹', '9')
    )
