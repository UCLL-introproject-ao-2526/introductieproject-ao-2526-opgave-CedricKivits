import hashlib
import itertools
import string

target_hash = "10ceee87f8b145ab495c3bca73b94455970159c6"

for combination in itertools.product(string.ascii_uppercase, repeat=7):
    password = "".join(combination)

    hashed_password = hashlib.sha1(password.encode()).hexdigest()

    if hashed_password == target_hash:
        print(f"Password found: {password}")
        break