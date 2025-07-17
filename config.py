import os
from pathlib import Path

# Directory configuration
BASE_DIR = Path(__file__).parent.resolve()
WORDLIST_DIR = BASE_DIR / "wordlists"

# Default algorithm
DEFAULT_ALGORITHM = "md5"

# Wordlist configuration
DEFAULT_WORDLIST = WORDLIST_DIR / "rockyou.txt"

COMMON_WORDLISTS = {
    "rockyou": str(WORDLIST_DIR / "rockyou.txt"),
    "common": str(WORDLIST_DIR / "common.txt"), 
    "darkweb": str(WORDLIST_DIR / "darkweb2017-top10000.txt"),
    "10mil": str(WORDLIST_DIR / "10-million-password-list-top-1000000.txt"),
    "fasttrack": str(WORDLIST_DIR / "fasttrack.txt")
}

# Performance settings
CHUNK_SIZE = 10000  # Words processed per chunk
MAX_WORKERS = os.cpu_count() or 4  # Default to 4 if cpu_count fails

# Output settings
SHOW_PROGRESS = True
VERBOSE_OUTPUT = False
