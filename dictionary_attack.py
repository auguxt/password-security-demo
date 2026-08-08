# Dictionary Attack
# Tries a list of common passwords one by one

import time

def dictionary_attack(target, wordlist):
    attempts = 0
    start = time.time()

    print(f"Trying to crack: {target}\n")

    for word in wordlist:
        attempts += 1
        print(f"Trying: {word}")

        if word == target:
            end = time.time()
            print(f"\nPassword found: {word}")
            print(f"Attempts: {attempts}")
            print(f"Time: {end - start:.2f} seconds")
            return

    print("\nPassword not found!")


# --- Load wordlist and try it out ---
with open("wordlist.txt", "r") as f:
    wordlist = [line.strip() for line in f]

dictionary_attack("letmein", wordlist)
