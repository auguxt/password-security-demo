# Brute Force Attack
# Tries every possible combination to guess a password

import itertools
import string
import time

def brute_force(target):
    # Use only lowercase letters and digits
    charset = string.ascii_lowercase + string.digits
    attempts = 0
    start = time.time()

    print(f"Trying to crack: {target}\n")

    for length in range(1, 6):  # Try lengths 1 to 5
        for guess in itertools.product(charset, repeat=length):
            guess = ''.join(guess)
            attempts += 1

            if guess == target:
                end = time.time()
                print(f"Password found: {guess}")
                print(f"Attempts: {attempts:,}")
                print(f"Time: {end - start:.2f} seconds")
                return

    print("Password not found!")


# --- Try it out ---
brute_force("ab3")
