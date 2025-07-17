# HashPot

A high-performance password hash cracker with multi-algorithm support.

## Features

- Supports MD5, SHA1, SHA256, SHA512
- Multi-core processing
- Progress tracking
- Predefined & custom wordlists
- Clean interrupt handling

## Quick Start

1. Install requirements:
```bash
pip install -r requirements.txt


## Download Wordlists 
mkdir -p wordlists
cd wordlists 
wget https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt -O wordlists/rockyou.txt

## Basic cracking 
python cli.py [HASH] -a [ALGORITHM]

## Advanced Options
python cli.py [HASH] -a sha256 -w custom_wordlist.txt -t 8 -v

