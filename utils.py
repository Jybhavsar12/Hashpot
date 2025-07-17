import re
import os
from typing import List

def load_wordlist(path: str) -> List[str]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Wordlist not found: {path}")
    
    with open(path, 'r', encoding='latin-1', errors='ignore') as f:
        return [line.strip() for line in f if line.strip()]

def hash_match(word: str, target_hash: str, algorithm) -> bool:
    return algorithm(word.encode()).hexdigest() == target_hash.lower()

def validate_hash(candidate: str, algorithm: str) -> bool:
    hash_patterns = {
        'md5': r'^[a-f0-9]{32}$',
        'sha1': r'^[a-f0-9]{40}$',
        'sha256': r'^[a-f0-9]{64}$',
        'sha512': r'^[a-f0-9]{128}$'
    }
    return bool(re.match(hash_patterns[algorithm], candidate.lower()))

def progress_bar(processed: int, total: int, length: int = 50):
    percent = ("{0:.1f}").format(100 * (processed / float(total)))
    filled = int(length * processed // total)
    bar = '█' * filled + '-' * (length - filled)
    print(f'\rProgress: |{bar}| {percent}%', end='\r')
def load_wordlist(path: str) -> List[str]:
    try:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Wordlist not found: {path}")
        
        with open(path, 'r', encoding='latin-1', errors='ignore') as f:
            return [line.strip() for line in f if line.strip()]
            
    except Exception as e:
        print(f"Error loading wordlist: {str(e)}")
        return []
