import random
import string

def generate_random_filename():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16)) + '.csv'