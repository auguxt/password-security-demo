#!/usr/bin/env python3
"""
🔐 Educational Brute Force Password Cracker

⚠️  WARNING: For educational purposes ONLY!
   Only use on passwords you own or have explicit permission to test.
   Unauthorized access to computer systems is illegal.

Author: Syed Sameer
License: MIT (Educational Use Only)
"""

import itertools
import string
import time
import sys
import argparse
from typing import Optional, Tuple
from datetime import timedelta

# ================= CONFIGURATION =================

class BruteForceConfig:
    """Configuration for brute force attack."""
    
    # Character sets
    DIGITS = string.digits                    # 0-9
    LOWERCASE = string.ascii_lowercase        # a-z
    UPPERCASE = string.ascii_uppercase        # A-Z
    SPECIAL = "!@#$%^&*()_+-=[]{}|;:,.<>?"   # Special characters
    
    # Default settings
    DEFAULT_MAX_LENGTH = 5
    DEFAULT_CHARSET = DIGITS + LOWERCASE
    PROGRESS_UPDATE_INTERVAL = 10000  # Show progress every N attempts


# ================= CORE FUNCTIONS =================

def generate_charset(use_digits: bool = True, 
                     use_lowercase: bool = True, 
                     use_uppercase: bool = False,
                     use_special: bool = False,
                     custom_chars: str = "") -> str:
    """Generate character set based on options."""
    charset = ""
    
    if use_digits:
        charset += BruteForceConfig.DIGITS
    if use_lowercase:
        charset += BruteForceConfig.LOWERCASE
    if use_uppercase:
        charset += BruteForceConfig.UPPERCASE
    if use_special:
        charset += BruteForceConfig.SPECIAL
    if custom_chars:
        charset += custom_chars
    
    if not charset:
        raise ValueError("At least one character type must be selected!")
    
    # Remove duplicates while preserving order
    return ''.join(dict.fromkeys(charset))

def calculate_total_combinations(charset: str, max_length: int) -> int:
    """Calculate total possible combinations to try."""
    total = 0
    for length in range(1, max_length + 1):
        total += len(charset) ** length
    return total

def format_time(seconds: float) -> str:
    """Format seconds into human-readable time."""
    if seconds < 60:
        return f"{seconds:.2f} seconds"
    elif seconds < 3600:
        return f"{seconds/60:.2f} minutes"
    else:
        return f"{seconds/3600:.2f} hours"

def brute_force_attack(target: str, 
                       charset: str, 
                       max_length: int,
                       show_progress: bool = True) -> Tuple[Optional[str], int, float]:
    """
    Perform brute force attack on target password.
    
    Returns:
        tuple: (found_password or None, attempts, time_taken)
    """
    attempts = 0
    start_time = time.time()
    found = False
    found_password = None
    
    # Calculate total for progress estimation
    total_combinations = calculate_total_combinations(charset, max_length)
    
    print(f"\n📊 Attack Configuration:")
    print(f"   Target Length: 1-{max_length} characters")
    print(f"   Character Set: {len(charset)} characters")
    print(f"   Total Combinations: {total_combinations:,}")
    print(f"   Estimated Time: {format_time(total_combinations / 100000)} (at 100k attempts/sec)")
    print("\n" + "🔐" * 30 + "\n")
    
    if show_progress:
        print("🚀 Starting brute force attack...\n")
    
    for length in range(1, max_length + 1):
        for guess_tuple in itertools.product(charset, repeat=length):
            guess = ''.join(guess_tuple)
            attempts += 1
            
            # Show progress (not every attempt - too slow!)
            if show_progress and attempts % BruteForceConfig.PROGRESS_UPDATE_INTERVAL == 0:
                elapsed = time.time() - start_time
                attempts_per_sec = attempts / elapsed if elapsed > 0 else 0
                progress = (attempts / total_combinations) * 100
                eta = (total_combinations - attempts) / attempts_per_sec if attempts_per_sec > 0 else 0
                
                print(f"\r📍 Progress: {progress:.2f}% | "
                      f"Attempts: {attempts:,} | "
                      f"Speed: {attempts_per_sec:,.0f}/s | "
                      f"ETA: {format_time(eta)}", end='', flush=True)
            
            if guess == target:
                end_time = time.time()
                found = True
                found_password = guess
                break
        
        if found:
            break
    
    end_time = time.time()
    time_taken = end_time - start_time
    
    return found_password, attempts, time_taken

def display_results(found_password: Optional[str], 
                    attempts: int, 
                    time_taken: float,
                    target: str) -> None:
    """Display attack results."""
    print("\n\n" + "🔐" * 30)
    
    if found_password:
        print("✅ PASSWORD FOUND!")
        print("🔐" * 30)
        print(f"   Password: {found_password}")
        print(f"   Attempts: {attempts:,}")
        print(f"   Time Taken: {format_time(time_taken)}")
        print(f"   Speed: {attempts/time_taken:,.0f} attempts/second")
        print(f"   Target Was: {target}")
    else:
        print("❌ PASSWORD NOT FOUND")
        print("🔐" * 30)
        print(f"   Attempts Made: {attempts:,}")
        print(f"   Time Elapsed: {format_time(time_taken)}")
        print(f"   Target: {target}")
        print(f"   Try increasing max_length or expanding character set")
    
    print("🔐" * 30 + "\n")

def print_security_warning() -> None:
    """Display important security and legal warning."""
    print("\n" + "⚠️" * 30)
    print("           LEGAL & ETHICAL WARNING")
    print("⚠️" * 30)
    print("""
🔴 This tool is for EDUCATIONAL PURPOSES ONLY!

✅ LEGAL USE CASES:
   • Testing YOUR OWN passwords
   • Learning cybersecurity concepts
   • CTF challenges with permission
   • Security research in controlled environments

❌ ILLEGAL USE CASES:
   • Accessing accounts without permission
   • Cracking passwords you don't own
   • Unauthorized system access
   • Any violation of computer crime laws

⚖️  LEGAL NOTICE:
   Unauthorized access to computer systems is a crime in most jurisdictions.
   You are solely responsible for how you use this tool.
   The authors are NOT responsible for any misuse.

📚 BETTER ALTERNATIVES FOR SECURITY:
   • Use password managers (Bitwarden, 1Password)
   • Enable 2FA/MFA on all accounts
   • Use long, random passwords (16+ characters)
   • Never reuse passwords across sites
""")
    print("⚠️" * 30 + "\n")


# ================= INTERACTIVE DEMO =================

def interactive_demo() -> None:
    """Run interactive brute force demonstration."""
    print_security_warning()
    
    print("\n" + "🔐" * 30)
    print("    Educational Brute Force Password Cracker")
    print("🔐" * 30 + "\n")
    
    # Get target password
    while True:
        target = input("Enter target password to crack: ").strip()
        if not target:
            print("❌ Password cannot be empty!")
            continue
        if len(target) > 8:
            confirm = input(f"⚠️  Password is {len(target)} chars. This may take a long time. Continue? (y/n): ").strip().lower()
            if confirm != 'y':
                continue
        break
    
    # Configure character set
    print("\n📋 Character Set Options:")
    print("  [1] Digits only (0-9)")
    print("  [2] Digits + Lowercase (0-9, a-z)")
    print("  [3] Digits + Lowercase + Uppercase")
    print("  [4] All characters (including special)")
    print("  [5] Custom character set")
    
    charset_choice = input("\nSelect option (1-5) [default: 2]: ").strip() or "2"
    
    if charset_choice == "1":
        charset = generate_charset(use_digits=True, use_lowercase=False)
    elif charset_choice == "3":
        charset = generate_charset(use_digits=True, use_lowercase=True, use_uppercase=True)
    elif charset_choice == "4":
        charset = generate_charset(use_digits=True, use_lowercase=True, use_uppercase=True, use_special=True)
    elif charset_choice == "5":
        charset = input("Enter custom characters: ").strip()
        if not charset:
            print("❌ Custom charset cannot be empty!")
            return
    else:
        charset = generate_charset(use_digits=True, use_lowercase=True)
    
    print(f"✅ Character set: {len(charset)} characters ({charset[:50]}{'...' if len(charset) > 50 else ''})")
    
    # Get max length
    while True:
        try:
            max_length = int(input("Enter maximum password length to try [default: 5]: ").strip() or "5")
            if max_length < 1 or max_length > 10:
                print("⚠️  Please enter a value between 1 and 10")
                continue
            if max_length > 6:
                confirm = input(f"⚠️  Length {max_length} may take hours/days. Continue? (y/n): ").strip().lower()
                if confirm != 'y':
                    continue
            break
        except ValueError:
            print("❌ Please enter a valid number!")
    
    # Progress display
    show_progress = input("\n📊 Show progress updates? (y/n) [default: y]: ").strip().lower() != 'n'
    
    # Run attack
    found_password, attempts, time_taken = brute_force_attack(
        target=target,
        charset=charset,
        max_length=max_length,
        show_progress=show_progress
    )
    
    # Display results
    display_results(found_password, attempts, time_taken, target)
    
    # Security recommendations
    if found_password:
        print("📚 SECURITY RECOMMENDATIONS:")
        print("   • Use passwords at least 12 characters long")
        print("   • Mix uppercase, lowercase, digits, and special chars")
        print("   • Use a password manager")
        print("   • Enable 2FA on all accounts")
        print("   • Never reuse passwords\n")


# ================= COMMAND LINE INTERFACE =================

def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="🔐 Educational Brute Force Password Cracker",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
⚠️  WARNING: For educational purposes ONLY!
   Only use on passwords you own or have permission to test.

Examples:
  python3 brute_force.py -t "a3" -l 3
  python3 brute_force.py -t "test" -l 5 --uppercase
  python3 brute_force.py -t "pass123" -l 8 --digits --lowercase --uppercase
        """
    )
    
    parser.add_argument('-t', '--target', type=str, help='Target password to crack')
    parser.add_argument('-l', '--length', type=int, default=5, help='Maximum password length (default: 5)')
    parser.add_argument('-d', '--digits', action='store_true', default=True, help='Include digits (default: True)')
    parser.add_argument('-lc', '--lowercase', action='store_true', default=True, help='Include lowercase (default: True)')
    parser.add_argument('-uc', '--uppercase', action='store_true', help='Include uppercase')
    parser.add_argument('-s', '--special', action='store_true', help='Include special characters')
    parser.add_argument('-c', '--custom', type=str, help='Custom character set')
    parser.add_argument('-q', '--quiet', action='store_true', help='Suppress progress output')
    parser.add_argument('-i', '--interactive', action='store_true', help='Run interactive mode')
    
    return parser.parse_args()


# ================= MAIN =================

def main() -> None:
    """Main entry point."""
    args = parse_arguments()
    
    # Interactive mode
    if args.interactive or not args.target:
        interactive_demo()
        return
    
    # Command line mode
    try:
        # Generate charset
        charset = generate_charset(
            use_digits=args.digits,
            use_lowercase=args.lowercase,
            use_uppercase=args.uppercase,
            use_special=args.special,
            custom_chars=args.custom or ""
        )
        
        # Show warning
        print_security_warning()
        
        # Run attack
        found_password, attempts, time_taken = brute_force_attack(
            target=args.target,
            charset=charset,
            max_length=args.length,
            show_progress=not args.quiet
        )
        
        # Display results
        display_results(found_password, attempts, time_taken, args.target)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
