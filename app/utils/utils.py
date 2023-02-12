import faker


def generate_random_int(n):
    from random import randrange
    nums = [str(randrange(1, 10)) for _ in range(n)]
    return int(''.join(nums))


def generate_fake_url():
    fk = faker.Faker()
    fake_url = fk.url()[:-1]
    fake_file_path = fk.file_path(extension="mp4")
    return fake_url + fake_file_path
