# Password Hashing Demo
# Shows how passwords are stored safely

import hashlib
import bcrypt

def hash_md5(password):
    return hashlib.md5(password.encode()).hexdigest()

def hash_sha256(password):
    return hashlib.sha256(password.encode()).hexdigest()

def hash_bcrypt(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)

def verify_bcrypt(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)


# --- Try it out ---
password = "hello"

md5    = hash_md5(password)
sha256 = hash_sha256(password)
hashed = hash_bcrypt(password)

print(f"Password: {password}\n")
print(f"MD5:    {md5}   ❌ Weak")
print(f"SHA256: {sha256}   ⚠️  OK")
print(f"bcrypt: {hashed.decode()}   ✅ Best\n")

# Verify bcrypt
if verify_bcrypt(password, hashed):
    print("bcrypt verified: ✅ Password matches!")
else:
    print("bcrypt verified: ❌ Wrong password!")
