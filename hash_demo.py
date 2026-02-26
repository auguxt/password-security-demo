#!/usr/bin/env python3
"""
🔐 Educational Password Hashing Tool

Learn about password hashing algorithms, security levels, and best practices.

⚠️  WARNING: For educational purposes ONLY!
   Never store passwords in plain text.
   Always use secure hashing in production.

Author: Syed Sameer
License: MIT (Educational Use Only)
"""

import hashlib
import bcrypt
import time
import sys
import argparse
import os
import secrets
from typing import Optional, Tuple, Dict, List
from datetime import datetime

# ================= CONFIGURATION =================

class HashingConfig:
    """Configuration for password hashing."""
    
    # bcrypt work factor (higher = more secure but slower)
    BCRYPT_ROUNDS = 12
    
    # Minimum password requirements
    MIN_PASSWORD_LENGTH = 8
    RECOMMENDED_PASSWORD_LENGTH = 16
    
    # Hash algorithm info
    HASH_INFO = {
        "md5": {
            "name": "MD5",
            "bits": 128,
            "hex_length": 32,
            "security": "🔴 BROKEN - Do not use for passwords",
            "speed": "⚡ Very Fast",
            "use_case": "File integrity checks (not passwords)"
        },
        "sha1": {
            "name": "SHA1",
            "bits": 160,
            "hex_length": 40,
            "security": "🔴 WEAK - Deprecated for security",
            "speed": "⚡ Very Fast",
            "use_case": "Git commits, legacy systems"
        },
        "sha256": {
            "name": "SHA256",
            "bits": 256,
            "hex_length": 64,
            "security": "🟡 OK - But not for passwords alone",
            "speed": "⚡ Fast",
            "use_case": "Digital signatures, certificates"
        },
        "sha512": {
            "name": "SHA512",
            "bits": 512,
            "hex_length": 128,
            "security": "🟡 OK - But not for passwords alone",
            "speed": "⚡ Fast",
            "use_case": "High-security applications"
        },
        "bcrypt": {
            "name": "bcrypt",
            "bits": 184,
            "hex_length": 60,
            "security": "🟢 EXCELLENT - Recommended for passwords",
            "speed": "🐌 Intentionally Slow",
            "use_case": "Password storage (production)"
        },
        "pbkdf2": {
            "name": "PBKDF2",
            "bits": 256,
            "hex_length": 64,
            "security": "🟢 GOOD - Acceptable for passwords",
            "speed": "🐌 Slow (configurable)",
            "use_case": "Password storage, key derivation"
        },
        "argon2": {
            "name": "Argon2",
            "bits": 256,
            "hex_length": 64,
            "security": "🟢 BEST - Modern standard",
            "speed": "🐌 Very Slow (configurable)",
            "use_case": "Password storage (modern apps)"
        }
    }


# ================= HASHING FUNCTIONS =================

def hash_with_md5(password: str) -> str:
    """Hash password with MD5 (NOT recommended for passwords)."""
    return hashlib.md5(password.encode('utf-8')).hexdigest()

def hash_with_sha1(password: str) -> str:
    """Hash password with SHA1 (NOT recommended for passwords)."""
    return hashlib.sha1(password.encode('utf-8')).hexdigest()

def hash_with_sha256(password: str) -> str:
    """Hash password with SHA256 (better but still not ideal for passwords)."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def hash_with_sha512(password: str) -> str:
    """Hash password with SHA512."""
    return hashlib.sha512(password.encode('utf-8')).hexdigest()

def hash_with_bcrypt(password: str, rounds: int = HashingConfig.BCRYPT_ROUNDS) -> Tuple[bytes, bytes]:
    """
    Hash password with bcrypt (recommended for passwords).
    
    Returns:
        tuple: (hashed_password, salt)
    """
    salt = bcrypt.gensalt(rounds=rounds)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed, salt

def hash_with_pbkdf2(password: str, salt: bytes = None, iterations: int = 100000) -> Tuple[str, bytes]:
    """
    Hash password with PBKDF2-SHA256.
    
    Returns:
        tuple: (hashed_password_hex, salt)
    """
    if salt is None:
        salt = secrets.token_bytes(16)
    
    hashed = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        iterations
    )
    return hashed.hex(), salt

def verify_bcrypt(password: str, hashed: bytes) -> bool:
    """Verify password against bcrypt hash."""
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed)
    except Exception as e:
        print(f"❌ Verification error: {e}")
        return False

def verify_pbkdf2(password: str, hashed_hex: str, salt: bytes, iterations: int = 100000) -> bool:
    """Verify password against PBKDF2 hash."""
    try:
        new_hash, _ = hash_with_pbkdf2(password, salt, iterations)
        return secrets.compare_digest(new_hash, hashed_hex)
    except Exception as e:
        print(f"❌ Verification error: {e}")
        return False


# ================= ANALYSIS FUNCTIONS =================

def analyze_password_strength(password: str) -> Dict[str, any]:
    """Analyze password strength and provide recommendations."""
    analysis = {
        "length": len(password),
        "has_upper": any(c.isupper() for c in password),
        "has_lower": any(c.islower() for c in password),
        "has_digit": any(c.isdigit() for c in password),
        "has_special": any(not c.isalnum() for c in password),
        "score": 0,
        "rating": "",
        "recommendations": []
    }
    
    # Calculate score
    if analysis["length"] >= 8:
        analysis["score"] += 20
    if analysis["length"] >= 12:
        analysis["score"] += 20
    if analysis["length"] >= 16:
        analysis["score"] += 20
    if analysis["has_upper"]:
        analysis["score"] += 10
    if analysis["has_lower"]:
        analysis["score"] += 10
    if analysis["has_digit"]:
        analysis["score"] += 10
    if analysis["has_special"]:
        analysis["score"] += 10
    
    # Determine rating
    if analysis["score"] >= 90:
        analysis["rating"] = "🟢 EXCELLENT"
    elif analysis["score"] >= 70:
        analysis["rating"] = "🟡 GOOD"
    elif analysis["score"] >= 50:
        analysis["rating"] = "🟠 FAIR"
    else:
        analysis["rating"] = "🔴 WEAK"
    
    # Generate recommendations
    if analysis["length"] < 12:
        analysis["recommendations"].append("• Increase length to at least 12 characters")
    if not analysis["has_upper"]:
        analysis["recommendations"].append("• Add uppercase letters (A-Z)")
    if not analysis["has_lower"]:
        analysis["recommendations"].append("• Add lowercase letters (a-z)")
    if not analysis["has_digit"]:
        analysis["recommendations"].append("• Add numbers (0-9)")
    if not analysis["has_special"]:
        analysis["recommendations"].append("• Add special characters (!@#$%^&*)")
    
    # Check for common patterns
    common_patterns = ["password", "123456", "qwerty", "admin", "letmein"]
    if any(pattern in password.lower() for pattern in common_patterns):
        analysis["recommendations"].append("• Avoid common passwords and patterns")
    
    return analysis

def compare_hash_speeds(password: str, iterations: int = 100) -> Dict[str, float]:
    """Compare hashing speeds of different algorithms."""
    results = {}
    
    algorithms = {
        "MD5": hash_with_md5,
        "SHA1": hash_with_sha1,
        "SHA256": hash_with_sha256,
        "SHA512": hash_with_sha512,
    }
    
    for name, func in algorithms.items():
        start = time.time()
        for _ in range(iterations):
            func(password)
        end = time.time()
        results[name] = (end - start) / iterations * 1000  # ms per hash
    
    # bcrypt (fewer iterations due to slowness)
    start = time.time()
    for _ in range(10):
        hash_with_bcrypt(password)
    end = time.time()
    results["bcrypt"] = (end - start) / 10 * 1000
    
    return results

def generate_hash_comparison(password: str) -> List[Dict[str, str]]:
    """Generate comparison table of all hash algorithms."""
    comparison = []
    
    # Fast hashes
    comparison.append({
        "Algorithm": "MD5",
        "Hash": hash_with_md5(password),
        "Security": HashingConfig.HASH_INFO["md5"]["security"],
        "Speed": HashingConfig.HASH_INFO["md5"]["speed"]
    })
    
    comparison.append({
        "Algorithm": "SHA1",
        "Hash": hash_with_sha1(password),
        "Security": HashingConfig.HASH_INFO["sha1"]["security"],
        "Speed": HashingConfig.HASH_INFO["sha1"]["speed"]
    })
    
    comparison.append({
        "Algorithm": "SHA256",
        "Hash": hash_with_sha256(password),
        "Security": HashingConfig.HASH_INFO["sha256"]["security"],
        "Speed": HashingConfig.HASH_INFO["sha256"]["speed"]
    })
    
    comparison.append({
        "Algorithm": "SHA512",
        "Hash": hash_with_sha512(password),
        "Security": HashingConfig.HASH_INFO["sha512"]["security"],
        "Speed": HashingConfig.HASH_INFO["sha512"]["speed"]
    })
    
    # Password-specific hashes
    bcrypt_hash, _ = hash_with_bcrypt(password)
    comparison.append({
        "Algorithm": "bcrypt",
        "Hash": bcrypt_hash.decode()[:50] + "...",
        "Security": HashingConfig.HASH_INFO["bcrypt"]["security"],
        "Speed": HashingConfig.HASH_INFO["bcrypt"]["speed"]
    })
    
    pbkdf2_hash, _ = hash_with_pbkdf2(password)
    comparison.append({
        "Algorithm": "PBKDF2",
        "Hash": pbkdf2_hash[:50] + "...",
        "Security": HashingConfig.HASH_INFO["pbkdf2"]["security"],
        "Speed": HashingConfig.HASH_INFO["pbkdf2"]["speed"]
    })
    
    return comparison


# ================= DISPLAY FUNCTIONS =================

def print_banner():
    """Print application banner."""
    print("\n" + "🔐" * 35)
    print("        Educational Password Hashing Tool")
    print("🔐" * 35 + "\n")

def print_security_warning():
    """Display important security warning."""
    print("\n" + "⚠️" * 35)
    print("              SECURITY WARNING")
    print("⚠️" * 35)
    print("""
🔴 IMPORTANT PASSWORD SECURITY RULES:

   ❌ NEVER store passwords in plain text
   ❌ NEVER use MD5/SHA1 for password storage
   ❌ NEVER roll your own crypto in production
   ❌ NEVER reuse passwords across sites

   ✅ ALWAYS use bcrypt, Argon2, or PBKDF2
   ✅ ALWAYS use unique salts per password
   ✅ ALWAYS use password managers
   ✅ ALWAYS enable 2FA/MFA

📚 This tool is for EDUCATIONAL PURPOSES ONLY!
   Consult security professionals for production systems.
""")
    print("⚠️" * 35 + "\n")

def display_hash_results(password: str, results: Dict[str, any]) -> None:
    """Display hashing results."""
    print("\n" + "🔐" * 35)
    print("              HASH RESULTS")
    print("🔐" * 35)
    print(f"\n📝 Original Password: {password}")
    print(f"📏 Password Length: {len(password)} characters\n")
    
    print("┌─────────────┬──────────────────────────────────────────────────────┐")
    print("│ Algorithm   │ Hash                                                 │")
    print("├─────────────┼──────────────────────────────────────────────────────┤")
    
    for algo, hash_value in results.items():
        if isinstance(hash_value, bytes):
            hash_value = hash_value.decode()
        # Truncate long hashes for display
        display_hash = hash_value[:50] + "..." if len(hash_value) > 50 else hash_value
        print(f"│ {algo:<11} │ {display_hash:<52} │")
    
    print("└─────────────┴──────────────────────────────────────────────────────┘\n")

def display_password_analysis(analysis: Dict[str, any]) -> None:
    """Display password strength analysis."""
    print("\n" + "📊" * 35)
    print("          PASSWORD STRENGTH ANALYSIS")
    print("📊" * 35)
    
    print(f"\n🎯 Strength Rating: {analysis['rating']}")
    print(f"📈 Score: {analysis['score']}/100\n")
    
    print("┌─────────────────────┬──────────────┐")
    print("│ Criteria            │ Status       │")
    print("├─────────────────────┼──────────────┤")
    print(f"│ Length (≥8)         │ {'✅ Yes' if analysis['length'] >= 8 else '❌ No':<12} │")
    print(f"│ Length (≥12)        │ {'✅ Yes' if analysis['length'] >= 12 else '❌ No':<12} │")
    print(f"│ Length (≥16)        │ {'✅ Yes' if analysis['length'] >= 16 else '❌ No':<12} │")
    print(f"│ Uppercase (A-Z)     │ {'✅ Yes' if analysis['has_upper'] else '❌ No':<12} │")
    print(f"│ Lowercase (a-z)     │ {'✅ Yes' if analysis['has_lower'] else '❌ No':<12} │")
    print(f"│ Digits (0-9)        │ {'✅ Yes' if analysis['has_digit'] else '❌ No':<12} │")
    print(f"│ Special (!@#$%)     │ {'✅ Yes' if analysis['has_special'] else '❌ No':<12} │")
    print("└─────────────────────┴──────────────┘\n")
    
    if analysis['recommendations']:
        print("💡 Recommendations to Improve:")
        for rec in analysis['recommendations']:
            print(f"   {rec}")
        print()

def display_hash_comparison(comparison: List[Dict[str, str]]) -> None:
    """Display hash algorithm comparison."""
    print("\n" + "📊" * 35)
    print("          HASH ALGORITHM COMPARISON")
    print("📊" * 35)
    
    print("\n┌───────────┬────────────┬──────────────────────────────────────┬─────────────┐")
    print("│ Algorithm │ Security   │ Speed                                │ Use Case    │")
    print("├───────────┼────────────┼──────────────────────────────────────┼─────────────┤")
    
    for item in comparison:
        algo = item['Algorithm']
        security = HashingConfig.HASH_INFO.get(algo.lower(), {}).get('security', 'Unknown')
        speed = HashingConfig.HASH_INFO.get(algo.lower(), {}).get('speed', 'Unknown')
        use_case = HashingConfig.HASH_INFO.get(algo.lower(), {}).get('use_case', 'Unknown')
        
        # Truncate for display
        security_display = security[:38] + "..." if len(security) > 38 else security
        use_case_display = use_case[:11] + "..." if len(use_case) > 11 else use_case
        
        print(f"│ {algo:<9} │ {security_display:<38} │ {speed:<11} │ {use_case_display:<11} │")
    
    print("└───────────┴────────────┴──────────────────────────────────────┴─────────────┘\n")

def display_speed_comparison(speeds: Dict[str, float]) -> None:
    """Display hash speed comparison."""
    print("\n" + "⚡" * 35)
    print("          HASHING SPEED COMPARISON")
    print("⚡" * 35)
    print("\n⏱️  Time per hash (lower = faster):\n")
    
    # Sort by speed
    sorted_speeds = sorted(speeds.items(), key=lambda x: x[1])
    
    for algo, time_ms in sorted_speeds:
        bar_length = int(50 * (time_ms / max(speeds.values())))
        bar = "█" * bar_length + "░" * (50 - bar_length)
        print(f"   {algo:<10} │ {bar} │ {time_ms:.2f}ms")
    
    print("\n💡 Note: Slower is BETTER for password hashing!")
    print("   Fast hashes (MD5, SHA) are vulnerable to brute force.\n")


# ================= INTERACTIVE DEMO =================

def interactive_demo() -> None:
    """Run interactive password hashing demonstration."""
    print_banner()
    print_security_warning()
    
    # Get password
    while True:
        password = input("🔑 Enter password to hash: ").strip()
        if not password:
            print("❌ Password cannot be empty!")
            continue
        if len(password) < HashingConfig.MIN_PASSWORD_LENGTH:
            print(f"⚠️  Warning: Password is shorter than recommended ({HashingConfig.MIN_PASSWORD_LENGTH}+ chars)")
            confirm = input("Continue anyway? (y/n): ").strip().lower()
            if confirm != 'y':
                continue
        break
    
    # Analyze password
    analysis = analyze_password_strength(password)
    display_password_analysis(analysis)
    
    # Choose hashing options
    print("\n📋 Hashing Options:")
    print("  [1] Hash with all algorithms")
    print("  [2] Hash with secure algorithms only (bcrypt, PBKDF2)")
    print("  [3] Compare hash speeds")
    print("  [4] Verify existing hash")
    print("  [5] Generate secure password")
    
    choice = input("\nSelect option (1-5) [default: 1]: ").strip() or "1"
    
    if choice == "1":
        # Hash with all algorithms
        print("\n🔄 Generating hashes...\n")
        start = time.time()
        
        results = {
            "MD5": hash_with_md5(password),
            "SHA1": hash_with_sha1(password),
            "SHA256": hash_with_sha256(password),
            "SHA512": hash_with_sha512(password),
        }
        
        bcrypt_hash, _ = hash_with_bcrypt(password)
        results["bcrypt"] = bcrypt_hash
        
        pbkdf2_hash, _ = hash_with_pbkdf2(password)
        results["PBKDF2"] = pbkdf2_hash
        
        end = time.time()
        
        display_hash_results(password, results)
        print(f"✅ All hashes generated in {end - start:.4f} seconds")
        
        # Verify bcrypt
        print("\n🧪 Verifying bcrypt hash...")
        if verify_bcrypt(password, bcrypt_hash):
            print("✅ bcrypt Verification: Success")
        else:
            print("❌ bcrypt Verification: Failed")
        
        # Show comparison
        display_hash_comparison(generate_hash_comparison(password))
        
    elif choice == "2":
        # Secure algorithms only
        print("\n🔄 Generating secure hashes...\n")
        
        bcrypt_hash, bcrypt_salt = hash_with_bcrypt(password)
        pbkdf2_hash, pbkdf2_salt = hash_with_pbkdf2(password)
        
        print("🔐 bcrypt Hash:")
        print(f"   {bcrypt_hash.decode()}\n")
        print("🔐 PBKDF2 Hash:")
        print(f"   {pbkdf2_hash}\n")
        print("💡 These are recommended for production password storage!\n")
        
    elif choice == "3":
        # Speed comparison
        print("\n⏱️  Running speed comparison (this may take a moment)...\n")
        speeds = compare_hash_speeds(password)
        display_speed_comparison(speeds)
        
    elif choice == "4":
        # Verify existing hash
        print("\n🔍 Hash Verification")
        hash_type = input("Enter hash type (bcrypt/pbkdf2): ").strip().lower()
        existing_hash = input("Enter existing hash: ").strip()
        test_password = input("Enter password to verify: ").strip()
        
        if hash_type == "bcrypt":
            if verify_bcrypt(test_password, existing_hash.encode()):
                print("✅ Password matches hash!")
            else:
                print("❌ Password does not match hash!")
        elif hash_type == "pbkdf2":
            # Would need salt for proper verification
            print("⚠️  PBKDF2 verification requires salt. Use interactive mode for full demo.")
        else:
            print("❌ Unknown hash type!")
            
    elif choice == "5":
        # Generate secure password
        print("\n🎲 Generating secure passwords...\n")
        for i in range(5):
            secure_password = ''.join(secrets.choice(
                string.ascii_letters + string.digits + "!@#$%^&*()"
            ) for _ in range(16))
            print(f"   {i+1}. {secure_password}")
        print("\n💡 Save these securely! They cannot be recovered.\n")

def generate_secure_password(length: int = 16, use_special: bool = True) -> str:
    """Generate a cryptographically secure random password."""
    import string
    chars = string.ascii_letters + string.digits
    if use_special:
        chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    return ''.join(secrets.choice(chars) for _ in range(length))


# ================= COMMAND LINE INTERFACE =================

def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="🔐 Educational Password Hashing Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
⚠️  WARNING: For educational purposes ONLY!
   Never use MD5/SHA1 for password storage in production.

Examples:
  python3 password_hashing.py -p "MyPassword123"
  python3 password_hashing.py -p "test" --analyze
  python3 password_hashing.py --generate
  python3 password_hashing.py --compare
  python3 password_hashing.py --interactive
        """
    )
    
    parser.add_argument('-p', '--password', type=str, help='Password to hash')
    parser.add_argument('-a', '--analyze', action='store_true', help='Analyze password strength')
    parser.add_argument('-c', '--compare', action='store_true', help='Compare hash algorithms')
    parser.add_argument('-s', '--speed', action='store_true', help='Compare hash speeds')
    parser.add_argument('-g', '--generate', action='store_true', help='Generate secure password')
    parser.add_argument('-n', '--count', type=int, default=5, help='Number of passwords to generate')
    parser.add_argument('-l', '--length', type=int, default=16, help='Password length for generation')
    parser.add_argument('-i', '--interactive', action='store_true', help='Run interactive mode')
    parser.add_argument('-q', '--quiet', action='store_true', help='Minimal output')
    
    return parser.parse_args()


# ================= MAIN =================

def main() -> None:
    """Main entry point."""
    args = parse_arguments()
    
    # Interactive mode
    if args.interactive or not args.password:
        interactive_demo()
        return
    
    # Show warning
    print_banner()
    print_security_warning()
    
    # Generate password
    if args.generate:
        print(f"\n🎲 Generating {args.count} secure password(s) ({args.length} chars)...\n")
        for i in range(args.count):
            password = generate_secure_password(args.length)
            print(f"   {i+1}. {password}")
        print("\n💡 Save these securely!\n")
        return
    
    # Hash password
    password = args.password
    
    # Analyze password
    if args.analyze:
        analysis = analyze_password_strength(password)
        display_password_analysis(analysis)
    
    # Generate hashes
    print("\n🔄 Generating hashes...\n")
    start = time.time()
    
    results = {
        "MD5": hash_with_md5(password),
        "SHA1": hash_with_sha1(password),
        "SHA256": hash_with_sha256(password),
        "SHA512": hash_with_sha512(password),
    }
    
    bcrypt_hash, _ = hash_with_bcrypt(password)
    results["bcrypt"] = bcrypt_hash
    
    pbkdf2_hash, _ = hash_with_pbkdf2(password)
    results["PBKDF2"] = pbkdf2_hash
    
    end = time.time()
    
    if not args.quiet:
        display_hash_results(password, results)
        print(f"✅ All hashes generated in {end - start:.4f} seconds\n")
    
    # Compare algorithms
    if args.compare:
        display_hash_comparison(generate_hash_comparison(password))
    
    # Compare speeds
    if args.speed:
        print("⏱️  Running speed comparison...\n")
        speeds = compare_hash_speeds(password)
        display_speed_comparison(speeds)
    
    # Verify bcrypt
    print("\n🧪 Verifying bcrypt hash...")
    if verify_bcrypt(password, bcrypt_hash):
        print("✅ bcrypt Verification: Success\n")
    else:
        print("❌ bcrypt Verification: Failed\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
