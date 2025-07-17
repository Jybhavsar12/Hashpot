#!/usr/bin/env python3
import hashlib
import multiprocessing
import signal
import sys
from typing import Optional, Callable, Dict, List

class HashCracker:
    def __init__(self):
        self.stop_cracking = False
        signal.signal(signal.SIGINT, self._handle_interrupt)
        
        # Replace lambdas with proper methods for serialization
        self.algorithms: Dict[str, str] = {
            'md5': 'md5',
            'sha1': 'sha1', 
            'sha256': 'sha256',
            'sha512': 'sha512'
        }
    
    def _handle_interrupt(self, signum, frame):
        self.stop_cracking = True
    
    def _hash_function(self, algorithm: str, data: bytes) -> bytes:
        """Replacement for lambda functions that can be pickled"""
        return getattr(hashlib, algorithm)(data).digest()
    
    def crack(self, target_hash: str, wordlist_path: str, workers: int = 4,
             callback: Optional[Callable] = None) -> Optional[str]:
        try:
            # Convert hex hash to bytes if it's hex
            try:
                target_bin = bytes.fromhex(target_hash)
            except ValueError:
                target_bin = target_hash.encode()
            
            with multiprocessing.Pool(workers) as pool:
                for chunk in self._chunk_generator(wordlist_path, 10000):
                    if self.stop_cracking:
                        pool.terminate()
                        return None
                    
                    results = pool.imap_unordered(
                        self._check_word,
                        [(word, target_bin, algo) for word in chunk for algo in self.algorithms.values()],
                        chunksize=1000
                    )
                    
                    for i, result in enumerate(results, 1):
                        if callback:
                            callback(i)
                        if result:
                            pool.terminate()
                            return result
                           
        except KeyboardInterrupt:
            return None
        return None
    
    def _chunk_generator(self, wordlist_path: str, chunk_size: int):
        chunk = []
        with open(wordlist_path, 'r', errors='ignore') as f:
            for line in f:
                if self.stop_cracking:
                    break
                chunk.append(line.strip())
                if len(chunk) >= chunk_size:
                    yield chunk
                    chunk = []
            if chunk:
                yield chunk
    
    def _check_word(self, args) -> Optional[str]:
        word, target_bin, algorithm = args
        try:
            if self._hash_function(algorithm, word.encode()) == target_bin:
                return word
        except:
            pass
        return None

if __name__ == "__main__":
    print("Run through cli.py instead", file=sys.stderr)
    sys.exit(1)
