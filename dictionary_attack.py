#!/usr/bin/env python3
"""
🔐 Educational Dictionary Password Attack Tool

⚠️  WARNING: For educational purposes ONLY!
   Only use on passwords you own or have explicit permission to test.
   Unauthorized access to computer systems is illegal.

Author: Syed Sameer
License: MIT (Educational Use Only)
"""

import time
import sys
import argparse
import os
from typing import Optional, List, Tuple
from datetime import timedelta

# ================= CONFIGURATION =================

class DictionaryAttackConfig:
    """Configuration for dictionary attack."""
    
    # Default wordlist path
    DEFAULT_WORDLIST = "wordlist.txt"
    
    # Common passwords (built-in mini wordlist)
    COMMON_PASSWORDS = [
        "123456", "password", "12345678", "qwerty", "123456789",
        "12345", "1234", "111111", "1234567", "dragon",
        "123123", "baseball", "iloveyou", "football", "sunshine",
        "princess", "welcome", "shadow", "hunter", "superman",
        "admin", "letmein", "monkey", "master", "access",
        "mustang", "696969", "654321", "smiley", "batman",
        "trustno1", "cheese", "passw0rd", "hello", "charlie",
        "donald", "password1", "qwerty123", "loveme", "jesus",
        "shadowhunter", "rockyou", "michael", "ashley", "bailey"
    ]
    
    # Progress update interval
    PROGRESS_UPDATE_INTERVAL = 100
    
    # Simulated delay (for educational purposes)
    DEFAULT_DELAY = 0.0
    MAX_RECOMMENDED_DELAY = 1.0


# ================= WORDLIST FUNCTIONS =================

def load_wordlist_from_file(filepath: str) -> List[str]:
    """Load passwords from a text file (one per line)."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"❌ Wordlist file not found: {filepath}")
    
    wordlist = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                word = line.strip()
                if word:  # Skip empty lines
                    wordlist.append(word)
        
        if not wordlist:
            raise ValueError("❌ Wordlist file is empty!")
        
        return wordlist
    
    except PermissionError:
        raise PermissionError(f"❌ Permission denied: {filepath}")
    except Exception as e:
        raise Exception(f"❌ Error reading wordlist: {e}")

def get_wordlist(source: str = "builtin", 
                 filepath: str = "",
                 custom_words: List[str] = None) -> List[str]:
    """
    Get wordlist from various sources.
    
    Args:
        source: "builtin", "file", or "custom"
        filepath: Path to wordlist file (if source="file")
        custom_words: List of custom words (if source="custom")
    
    Returns:
        List of passwords to try
    """
    if source == "builtin":
        return DictionaryAttackConfig.COMMON_PASSWORDS.copy()
    
    elif source == "file":
        if not filepath:
            filepath = DictionaryAttackConfig.DEFAULT_WORDLIST
        return load_wordlist_from_file(filepath)
    
    elif source == "custom":
        if not custom_words:
            raise ValueError("❌ No custom words provided!")
        return custom_words
    
    elif source == "combined":
        # Combine builtin + file
        wordlist = DictionaryAttackConfig.COMMON_PASSWORDS.copy()
        if filepath and os.path.exists(filepath):
            try:
                file_words = load_wordlist_from_file(filepath)
                wordlist.extend(file_words)
                # Remove duplicates while preserving order
                wordlist = list(dict.fromkeys(wordlist))
            except:
                pass
        return wordlist
    
    else:
        raise ValueError(f"❌ Unknown wordlist source: {source}")

def save_wordlist(wordlist: List[str], filepath: str = "wordlist.txt") -> bool:
    """Save wordlist to file."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            for word in wordlist:
                f.write(word + '\n')
        print(f"✅ Wordlist saved to: {filepath} ({len(wordlist)} words)")
        return True
    except Exception as e:
        print(f"❌ Save failed: {e}")
        return False


# ================= ATTACK FUNCTIONS =================

def dictionary_attack(target: str, 
                      wordlist: List[str],
                      delay: float = 0.0,
                      show_progress: bool = True,
                      case_variations: bool = False) -> Tuple[Optional[str], int, float]:
    """
    Perform dictionary attack on target password.
    
    Args:
        target: Target password to crack
        wordlist: List of passwords to try
        delay: Delay between attempts (seconds)
        show_progress: Show progress updates
        case_variations: Try uppercase/lowercase variations
    
    Returns:
        tuple: (found_password or None, attempts, time_taken)
    """
    attempts = 0
    start_time = time.time()
    found = False
    found_password = None
    
    total_words = len(wordlist)
    
    # Calculate expanded wordlist if case variations enabled
    if case_variations:
        # Each word could have multiple variations
        estimated_attempts = total_words * 3  # rough estimate (lower, upper, title)
    else:
        estimated_attempts = total_words
    
    print(f"\n📊 Attack Configuration:")
    print(f"   Wordlist Size: {total_words:,} words")
    print(f"   Case Variations: {'✅ Yes' if case_variations else '❌ No'}")
    print(f"   Estimated Attempts: {estimated_attempts:,}")
    print(f"   Delay: {delay}s between attempts")
    if delay > 0:
        estimated_time = estimated_attempts * delay
        print(f"   Estimated Time: {format_time(estimated_time)}")
    print("\n" + "🔐" * 30 + "\n")
    
    if show_progress:
        print("🚀 Starting dictionary attack...\n")
    
    for word in wordlist:
        # Generate variations if enabled
        words_to_try = [word]
        if case_variations:
            if word != word.lower():
                words_to_try.append(word.lower())
            if word != word.upper():
                words_to_try.append(word.upper())
            if word != word.title():
                words_to_try.append(word.title())
        
        for guess in words_to_try:
            attempts += 1
            
            # Simulate delay (for educational purposes)
            if delay > 0:
                time.sleep(delay)
            
            # Show progress
            if show_progress and attempts % DictionaryAttackConfig.PROGRESS_UPDATE_INTERVAL == 0:
                elapsed = time.time() - start_time
                attempts_per_sec = attempts / elapsed if elapsed > 0 else 0
                progress = (attempts / estimated_attempts) * 100 if estimated_attempts > 0 else 0
                
                print(f"\r📍 Progress: {progress:.1f}% | "
                      f"Attempts: {attempts:,} | "
                      f"Speed: {attempts_per_sec:,.1f}/s", end='', flush=True)
            
            # Check match
            if guess == target:
                found = True
                found_password = guess
                break
        
        if found:
            break
    
    end_time = time.time()
    time_taken = end_time - start_time
    
    return found_password, attempts, time_taken


# ================= UTILITY FUNCTIONS =================

def format_time(seconds: float) -> str:
    """Format seconds into human-readable time."""
    if seconds < 60:
        return f"{seconds:.2f} seconds"
    elif seconds < 3600:
        return f"{seconds/60:.2f} minutes"
    else:
        return f"{seconds/3600:.2f} hours"

def display_results(found_password: Optional[str], 
                    attempts: int, 
                    time_taken: float,
                    target: str,
                    wordlist_size: int) -> None:
    """Display attack results."""
    print("\n\n" + "🔐" * 30)
    
    if found_password:
        print("✅ PASSWORD CRACKED!")
        print("🔐" * 30)
        print(f"   Password: {found_password}")
        print(f"   Attempts: {attempts:,}")
        print(f"   Time Taken: {format_time(time_taken)}")
        print(f"   Speed: {attempts/time_taken:,.1f} attempts/second")
        print(f"   Wordlist Size: {wordlist_size:,} words")
        print(f"   Success Rate: {(attempts/wordlist_size)*100:.2f}% of wordlist")
    else:
        print("❌ PASSWORD NOT FOUND")
        print("🔐" * 30)
        print(f"   Attempts Made: {attempts:,}")
        print(f"   Time Elapsed: {format_time(time_taken)}")
        print(f"   Wordlist Size: {wordlist_size:,} words")
        print(f"   Target: {target}")
        print(f"\n💡 Try:")
        print(f"   • Using a larger wordlist (rockyou.txt)")
        print(f"   • Adding custom words related to target")
        print(f"   • Enabling case variations")
        print(f"   • Combining multiple wordlists")
    
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
   • Auditing your own systems

❌ ILLEGAL USE CASES:
   • Accessing accounts without permission
   • Cracking passwords you don't own
   • Unauthorized system access
   • Any violation of computer crime laws

⚖️  LEGAL NOTICE:
   Unauthorized access to computer systems is a crime in most jurisdictions.
   You are solely responsible for how you use this tool.
   The authors are NOT responsible for any misuse.

📚 WHY DICTIONARY ATTACKS WORK:
   • People use common passwords
   • People use dictionary words
   • People use personal info (names, dates)
   • People reuse passwords across sites

🛡️ HOW TO PROTECT YOURSELF:
   • Use long, random passwords (16+ chars)
   • Use a password manager
   • Enable 2FA/MFA on all accounts
   • Never reuse passwords
   • Avoid dictionary words in passwords
""")
    print("⚠️" * 30 + "\n")

def display_wordlist_stats(wordlist: List[str]) -> None:
    """Display statistics about the wordlist."""
    if not wordlist:
        return
    
    lengths = [len(w) for w in wordlist]
    
    print("\n📊 Wordlist Statistics:")
    print(f"   Total Words: {len(wordlist):,}")
    print(f"   Min Length: {min(lengths)} chars")
    print(f"   Max Length: {max(lengths)} chars")
    print(f"   Avg Length: {sum(lengths)/len(lengths):.1f} chars")
    
    # Character type analysis
    has_digit = sum(1 for w in wordlist if any(c.isdigit() for c in w))
    has_upper = sum(1 for w in wordlist if any(c.isupper() for c in w))
    has_special = sum(1 for w in wordlist if any(not c.isalnum() for c in w))
    
    print(f"   With Digits: {has_digit:,} ({has_digit/len(wordlist)*100:.1f}%)")
    print(f"   With Uppercase: {has_upper:,} ({has_upper/len(wordlist)*100:.1f}%)")
    print(f"   With Special Chars: {has_special:,} ({has_special/len(wordlist)*100:.1f}%)")
    print()


# ================= INTERACTIVE DEMO =================

def interactive_demo() -> None:
    """Run interactive dictionary attack demonstration."""
    print_security_warning()
    
    print("\n" + "🔐" * 30)
    print("    Educational Dictionary Attack Tool")
    print("🔐" * 30 + "\n")
    
    # Get target password
    while True:
        target = input("Enter target password to crack: ").strip()
        if not target:
            print("❌ Password cannot be empty!")
            continue
        break
    
    # Choose wordlist source
    print("\n📋 Wordlist Source:")
    print("  [1] Built-in common passwords (50 words)")
    print("  [2] Load from file")
    print("  [3] Combined (built-in + file)")
    print("  [4] Custom wordlist (enter manually)")
    
    source_choice = input("\nSelect option (1-4) [default: 1]: ").strip() or "1"
    
    wordlist = []
    filepath = ""
    
    if source_choice == "1":
        wordlist = get_wordlist(source="builtin")
        print(f"✅ Using built-in wordlist ({len(wordlist)} words)")
    
    elif source_choice == "2":
        filepath = input("Enter wordlist file path [wordlist.txt]: ").strip() or "wordlist.txt"
        try:
            wordlist = get_wordlist(source="file", filepath=filepath)
            print(f"✅ Loaded {len(wordlist):,} words from {filepath}")
            display_wordlist_stats(wordlist)
        except Exception as e:
            print(f"❌ Error: {e}")
            print("⚠️  Falling back to built-in wordlist")
            wordlist = get_wordlist(source="builtin")
    
    elif source_choice == "3":
        filepath = input("Enter wordlist file path [wordlist.txt]: ").strip() or "wordlist.txt"
        wordlist = get_wordlist(source="combined", filepath=filepath)
        print(f"✅ Using combined wordlist ({len(wordlist):,} words)")
        display_wordlist_stats(wordlist)
    
    elif source_choice == "4":
        print("Enter passwords (one per line, empty line to finish):")
        custom_words = []
        while True:
            word = input("  > ").strip()
            if not word:
                break
            custom_words.append(word)
        if custom_words:
            wordlist = get_wordlist(source="custom", custom_words=custom_words)
            print(f"✅ Using custom wordlist ({len(wordlist)} words)")
        else:
            print("⚠️  No custom words entered. Using built-in wordlist")
            wordlist = get_wordlist(source="builtin")
    
    else:
        wordlist = get_wordlist(source="builtin")
    
    # Case variations
    case_var = input("\n🔤 Try case variations? (y/n) [default: n]: ").strip().lower() == 'y'
    
    # Delay
    try:
        delay = float(input("⏱️  Delay between attempts in seconds [0]: ").strip() or "0")
        if delay > DictionaryAttackConfig.MAX_RECOMMENDED_DELAY:
            print(f"⚠️  Warning: {delay}s delay will make this very slow!")
            confirm = input("Continue anyway? (y/n): ").strip().lower()
            if confirm != 'y':
                delay = 0
    except ValueError:
        print("⚠️  Invalid delay, using 0")
        delay = 0
    
    # Progress display
    show_progress = input("\n📊 Show progress updates? (y/n) [default: y]: ").strip().lower() != 'n'
    
    # Run attack
    found_password, attempts, time_taken = dictionary_attack(
        target=target,
        wordlist=wordlist,
        delay=delay,
        show_progress=show_progress,
        case_variations=case_var
    )
    
    # Display results
    display_results(found_password, attempts, time_taken, target, len(wordlist))
    
    # Security recommendations
    print("📚 SECURITY RECOMMENDATIONS:")
    print("   • Use passwords at least 12 characters long")
    print("   • Avoid dictionary words")
    print("   • Use a password manager (Bitwarden, 1Password)")
    print("   • Enable 2FA on all accounts")
    print("   • Never reuse passwords across sites")
    print("   • Consider using passphrases (4+ random words)")
    print()


# ================= COMMAND LINE INTERFACE =================

def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="🔐 Educational Dictionary Password Attack Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
⚠️  WARNING: For educational purposes ONLY!
   Only use on passwords you own or have permission to test.

Examples:
  python3 dictionary_attack.py -t "shadowhunter"
  python3 dictionary_attack.py -t "password" -w rockyou.txt
  python3 dictionary_attack.py -t "Test123" --case-variations
  python3 dictionary_attack.py -t "admin" -w wordlist.txt -d 0.1
  python3 dictionary_attack.py --interactive
        """
    )
    
    parser.add_argument('-t', '--target', type=str, help='Target password to crack')
    parser.add_argument('-w', '--wordlist', type=str, help='Wordlist file path')
    parser.add_argument('-s', '--source', type=str, default='builtin',
                       choices=['builtin', 'file', 'combined', 'custom'],
                       help='Wordlist source (default: builtin)')
    parser.add_argument('-d', '--delay', type=float, default=0.0,
                       help='Delay between attempts in seconds (default: 0)')
    parser.add_argument('-c', '--case-variations', action='store_true',
                       help='Try uppercase/lowercase variations')
    parser.add_argument('-q', '--quiet', action='store_true',
                       help='Suppress progress output')
    parser.add_argument('-i', '--interactive', action='store_true',
                       help='Run interactive mode')
    parser.add_argument('--stats', action='store_true',
                       help='Show wordlist statistics')
    
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
        # Show warning
        print_security_warning()
        
        # Get wordlist
        wordlist = get_wordlist(
            source=args.source,
            filepath=args.wordlist
        )
        
        # Show stats if requested
        if args.stats:
            display_wordlist_stats(wordlist)
        
        # Run attack
        found_password, attempts, time_taken = dictionary_attack(
            target=args.target,
            wordlist=wordlist,
            delay=args.delay,
            show_progress=not args.quiet,
            case_variations=args.case_variations
        )
        
        # Display results
        display_results(found_password, attempts, time_taken, args.target, len(wordlist))
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
