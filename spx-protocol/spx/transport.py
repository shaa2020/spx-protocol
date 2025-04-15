# spx/transport.py
# SPX Protocol NSF by Shaan (github.com/shaa2020)

import asyncio
import socket
from typing import Tuple, Dict
from .crypto import ChronoCrypt

class NeuralStreamFabric:
    def _init_(self, host: str, port: int):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host, port))
        self.crypt = ChronoCrypt()
        self.streams: Dict[str, Dict[str, Any]] = {}  # {stream_id: {priority, color}}

    async def send(self, data: bytes, key: bytes, addr: Tuple[str, int], stream_id: str):
        """Send with nebula stream prioritization."""
        stream = self.streams.get(stream_id, {"priority": 1.0, "color": "#ffffff"})
        encrypted = self.crypt.encrypt(data, key, int(time.time() * 1000))
        self.sock.sendto(encrypted, addr)
        stream["priority"] *= 0.9
        self.streams[stream_id] = stream

    async def receive(self, key: bytes) -> Tuple[bytes, Tuple[str, int], str]:
        """Receive with NSF."""
        loop = asyncio.get_event_loop()
        data, addr = await loop.sock_recvfrom(self.sock, 65535)
        decrypted = self.crypt.decrypt(data, key)
        stream_id = hashlib.sha256(data).hexdigest()[:8]
        stream = self.streams.get(stream_id, {"priority": 1.0, "color": "#ffffff"})
        stream["priority"] += 0.1
        self.streams[stream_id] = stream
        return decrypted, addr, stream_id

    def get_stream_color(self, stream_id: str) -> str:
        """Get nebula stream color."""
        return self.streams.get(stream_id, {"color": "#ffffff"})["color"]

    def close(self):
        self.sock.close()