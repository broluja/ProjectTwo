
def generate_random_int(n):
    from random import randrange
    nums = [str(randrange(1, 10)) for _ in range(n)]
    return int(''.join(nums))
