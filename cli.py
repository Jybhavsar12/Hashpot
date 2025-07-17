#!/usr/bin/env python3
import os
import argparse
import sys
import time
from typing import Optional

from cracker import HashCracker
from utils import load_wordlist, validate_hash
from config import DEFAULT_WORDLIST, COMMON_WORDLISTS

class CLI:
    def __init__(self):
        self.cracker = HashCracker()
        self.start_time = 0
        self.processed = 0
        self.total_words = 0

    def parse_args(self) -> argparse.Namespace:
        parser = argparse.ArgumentParser(
            description="HashPot - Advanced Password Hash Cracker",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        
        # Required arguments
        parser.add_argument("hash", help="Target hash to crack")
        
        # Wordlist options
        wordlist_group = parser.add_mutually_exclusive_group()
        wordlist_group.add_argument(
            "-w", "--wordlist",
            default=DEFAULT_WORDLIST,
            help="Path to custom wordlist file"
        )
        wordlist_group.add_argument(
            "-l", "--wordlist-name",
            choices=list(COMMON_WORDLISTS.keys()),
            help="Use a predefined wordlist"
        )
        
        # Algorithm options
        parser.add_argument(
            "-a", "--algorithm",
            default="md5",
            choices=["md5", "sha1", "sha256", "sha512"],
            help="Hash algorithm to use"
        )
        
        # Performance options
        parser.add_argument(
            "-t", "--threads",
            type=int,
            default=min(8, os.cpu_count() or 4),
            help="Number of worker threads"
        )
        
        # Output options
        parser.add_argument(
            "-v", "--verbose",
            action="store_true",
            help="Show detailed progress information"
        )
        
        return parser.parse_args()

    def print_stats(self) -> None:
        elapsed = time.time() - self.start_time
        rate = self.processed / elapsed if elapsed > 0 else 0
        print(f"\n[+] Stats: {self.processed:,} hashes in {elapsed:.2f}s "
              f"({rate:,.0f} hashes/sec)")

    def run(self) -> None:
        args = self.parse_args()
        
        try:
            # Validate input
            if not validate_hash(args.hash, args.algorithm):
                print(f"Error: Invalid {args.algorithm} hash format", file=sys.stderr)
                sys.exit(1)
            
            # Select wordlist
            wordlist_path = COMMON_WORDLISTS.get(args.wordlist_name, args.wordlist)
            try:
                self.total_words = sum(1 for _ in load_wordlist(wordlist_path))
            except FileNotFoundError:
                print(f"Error: Wordlist not found at {wordlist_path}", file=sys.stderr)
                sys.exit(1)
            
            # Start cracking
            print(f"[*] Cracking {args.algorithm.upper()} hash with "
                  f"{self.total_words:,} words...")
            self.start_time = time.time()
            
            result = self.cracker.crack(
                target_hash=args.hash,
                wordlist_path=wordlist_path,
                workers=args.threads,
                callback=self.update_progress
            )
            
            # Show results
            if result:
                print(f"\n[+] Success! Password found: {result}")
            else:
                print("\n[-] Password not found in wordlist")
            
            if args.verbose:
                self.print_stats()
                
        except KeyboardInterrupt:
            print("\n[!] Cracking interrupted by user")
            if args.verbose and self.start_time > 0:
                self.print_stats()
            sys.exit(1)
        except Exception as e:
            print(f"\n[!] Error: {str(e)}", file=sys.stderr)
            sys.exit(1)

    def update_progress(self, count: int) -> None:
        """Callback for progress updates"""
        self.processed = count
        if count % 1000 == 0:  # Update every 1000 attempts
            percent = (count / self.total_words) * 100
            print(f"\rProgress: {count:,}/{self.total_words:,} ({percent:.1f}%)", 
                  end="", flush=True)

if __name__ == "__main__":
    cli = CLI()
    cli.run()
