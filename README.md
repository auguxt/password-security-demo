# Password Security Demo 🔐

Three simple demos showing how passwords are cracked and how to store them safely.
Built with plain Python — easy to read and understand.

> ⚠️ **For learning only.** Do not use on accounts you don't own.

---

## What's Inside

```
password-security-demo/
│
├── brute_force_demo.py
├── dictionary_attack.py
├── hash_demo.py
│
├── wordlist.txt
│
├── README.md
├── requirements.txt
├── LICENSE
└── .gitignore
```

---

## The 3 Demos

### 💥 Brute Force
Tries every possible combination until it finds the password.
```
Trying: a, b, c ... aa, ab ... 1a, 1b ...
Found: abc in 3.2 seconds
```

### 📖 Dictionary Attack
Tries a list of common passwords one by one.
```
Trying: 123456 ... password ... letmein
Found: letmein in 0.01 seconds
```

### 🔒 Hash Demo
Shows how passwords are stored safely using hashing.
```
"hello"  →  MD5:    5d41402abc4b2a76b9719d911017c592
"hello"  →  bcrypt: $2b$12$... (different every time!)
```

---

## Setup

```bash
# Install the only dependency (bcrypt)
pip install -r requirements.txt
```

---

## How to Run

```bash
python brute_force_demo.py
python dictionary_attack.py
python hash_demo.py
```

---

## Example Output

**Brute Force**
```
Password found: ab3
Attempts: 1,234
Time: 2.5 seconds
```

**Dictionary Attack**
```
Password cracked: letmein
Attempts: 32
Time: 0.01 seconds
```

**Hash Demo**
```
MD5:    5d41402abc4b2a76b9719d911017c592  ❌ Weak
SHA256: 2cf24dba5fb0a30e26e83b2ac5b9e29e  ⚠️  OK
bcrypt: $2b$12$V86Xrs1yo4...              ✅ Recommended
```

---

## Why Does This Matter?

| Attack | Works On | Fails On |
|--------|----------|----------|
| Brute Force | Short passwords | Long passwords (12+ chars) |
| Dictionary | Common passwords | Random passwords |
| Both | MD5/SHA hashed passwords | bcrypt hashed passwords |

---

## Stay Safe

- ✅ Use passwords 12+ characters long
- ✅ Mix letters, numbers and symbols
- ✅ Use a password manager
- ✅ Turn on 2FA everywhere
- ❌ Never reuse passwords

---

## Requirements

- Python 3.6+
- `bcrypt` (see requirements.txt)

---

## License

MIT — see [LICENSE](LICENSE)
