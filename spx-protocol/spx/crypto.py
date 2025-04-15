# spx/crypto.py
# SPX Protocol cryptography by Shaan (github.com/shaa2020)

from typing import Tuple
from Crypto.Cipher import AES
import os
import hashlib
import time

class ChronoCrypt:
    def _init_(self):
        self.key_size = 32
        self.intents = ["connect", "create", "protect", "explore"]

    def generate_keypair(self, emotion: str = "neutral", intent: str = "connect") -> Tuple[bytes, bytes]:
        """Starforged keypair with emotion and intent."""
        if intent not in self.intents:
            intent = "connect"
        seed = hashlib.sha256((emotion + intent + str(time.time())).encode()).digest()
        private_key = seed
        public_key = hashlib.sha256(private_key).digest()
        return public_key, private_key

    def encrypt(self, data: bytes, key: bytes, timestamp: int) -> bytes:
        """Time-weaving encryption."""
        temporal_key = hashlib.sha256(key + str(timestamp).encode()).digest()
        nonce = os.urandom(12)
        cipher = AES.new(temporal_key, AES.MODE_GCM, nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        return nonce + ciphertext + tag

    def decrypt(self, data: bytes, key: bytes, timestamp: int = None) -> bytes:
        """Decrypt with temporal key."""
        temporal_key = hashlib.sha256(key + str(timestamp or int(time.time() * 1000)).encode()).digest()
        nonce = data[:12]
        tag = data[-16:]
        ciphertext = data[12:-16]
        cipher = AES.new(temporal_key, AES.MODE_GCM, nonce=nonce)
        return cipher.decrypt_and_verify(ciphertext, tag)

def chrono_encrypt(data: bytes, key: bytes, timestamp: int) -> bytes:
    return ChronoCrypt().encrypt(data, key, timestamp)

def chrono_decrypt(data: bytes, key: bytes, timestamp: int = None) -> bytes:
    return ChronoCrypt().decrypt(data, key, timestamp)

def merkle_forest_proof(msg_id: str) -> str:
    """Merkle forest proof."""
    return hashlib.sha256(msg_id.encode()).hexdigest()