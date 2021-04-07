import random


def generation_code():
    chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    length = 20
    password = ''
    for i in range(length):
        password += random.choice(chars)
    return password
