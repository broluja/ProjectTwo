"""Utility functions"""
import faker
from datetime import datetime
from dateutil.relativedelta import relativedelta


def generate_random_int(n: int = 6) -> int:
    """
    Function that generates random code made from n integer numbers
    Param n: number of integers
    Return: Five digit integer.
    """
    from random import randrange
    nums = [str(randrange(1, 10)) for _ in range(n)]
    return int(''.join(nums))


def generate_fake_url() -> str:
    """
    Function that generates fake url using faker library
    Return: Fake url, string.
    """
    fk = faker.Faker()
    fake_url = fk.url()[:-1]
    fake_file_path = fk.file_path(extension="mp4")
    return fake_url + fake_file_path


def get_day_before_one_month() -> str:
    """
    Calculate exact day one month ago.
    Return: Date, string.
    """
    current_date_time = datetime.now() - relativedelta(months=1)
    return current_date_time.strftime('%Y-%m-%d')


def validate_password(password: str) -> bool:
    """
    Function validates given string as password.
    Password must contain at least 8 characters
    and at least one Upper character. Also, password
    needs to have at least one integer number.
    """
    return len(password) >= 8 and any(char in password for char in "0123456789")
