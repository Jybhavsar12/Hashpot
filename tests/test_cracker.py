import unittest
from cracker import HashCracker
from utils import load_wordlist, hash_match

class TestHashCracker(unittest.TestCase):
    def setUp(self):
        self.cracker = HashCracker()
        self.test_words = ["password", "123456", "qwerty"]
    
    def test_md5_crack(self):
        self.assertEqual(
            self.cracker._check_hash(("password", "5f4dcc3b5aa765d61d8327deb882cf99")),
            "password"
        )

    def test_hash_match(self):
        self.assertTrue(hash_match(
            "password", 
            "5f4dcc3b5aa765d61d8327deb882cf99",
            hashlib.md5
        ))
