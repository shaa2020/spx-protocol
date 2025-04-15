# tests/test_crypto.py
# SPX Protocol crypto tests by Shaan (github.com/shaa2020)

import unittest
from spx.crypto import ChronoCrypt

class TestChronoCrypt(unittest.TestCase):
    def test_encrypt_decrypt(self):
        crypt = ChronoCrypt()
        key = b"testkey" * 4
        data = b"hello"
        ts = int(time.time() * 1000)
        encrypted = crypt.encrypt(data, key, ts)
        decrypted = crypt.decrypt(encrypted, key, ts)
        self.assertEqual(data, decrypted)