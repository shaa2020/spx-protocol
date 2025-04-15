# spx/protocol.py
# SPX Protocol by Shaan (github.com/shaa2020)

from typing import Dict, Any, Optional
import uuid
import time
from .holographic import HolographicDataLattice
from .crypto import chrono_encrypt, chrono_decrypt, merkle_forest_proof
from .cosmic import CosmicTrace

class SPXMessage:
    def _init_(
        self,
        msg_type: str,
        msg_id: str,
        data: Dict[str, Any],
        key: bytes,
        emotion: str = "neutral",
        intent: str = "connect",
        error: Optional[str] = None,
        requires_ack: bool = False,
        swarm_key: Optional[str] = None
    ):
        self.msg_type = msg_type
        self.msg_id = msg_id
        self.data = data
        self.key = key
        self.emotion = emotion
        self.intent = intent
        self.error = error
        self.requires_ack = requires_ack
        self.swarm_key = swarm_key or msg_id
        self.timestamp = int(time.time() * 1000)
        self.hdl = HolographicDataLattice()
        self.trace = CosmicTrace()

    @staticmethod
    def create_request(
        msg_type: str,
        data: Dict[str, Any],
        key: bytes,
        emotion: str = "neutral",
        intent: str = "connect",
        requires_ack: bool = False,
        swarm_key: Optional[str] = None
    ) -> 'SPXMessage':
        return SPXMessage(msg_type, str(uuid.uuid4()), data, key, emotion, intent, requires_ack=requires_ack, swarm_key=swarm_key)

    @staticmethod
    def create_response(
        original: 'SPXMessage',
        data: Dict[str, Any],
        key: bytes,
        error: Optional[str] = None
    ) -> 'SPXMessage':
        return SPXMessage(
            f"{original.msg_type}_RESP",
            original.msg_id,
            data,
            key,
            original.emotion,
            original.intent,
            error=error,
            requires_ack=original.requires_ack,
            swarm_key=original.swarm_key
        )

    def to_bytes(self) -> bytes:
        """Serialize to Chrono-Crypt HDL with astral tags."""
        with self.trace.span(f"serialize-{self.msg_type}"):
            header = {
                "type": self.msg_type,
                "id": self.msg_id,
                "timestamp": self.timestamp,
                "emotion": self.emotion,
                "intent": self.intent,
                "requires_ack": self.requires_ack,
                "swarm_key": self.swarm_key,
                "error": self.error,
                "proof": merkle_forest_proof(self.msg_id),
                "astral_tag": f"{self.emotion}:{self.intent}"
            }
            header_bytes = self.hdl.encode(header)
            encrypted_header = chrono_encrypt(header_bytes, self.key, self.timestamp)
            data_bytes = self.hdl.encode(self.data)
            encrypted_data = chrono_encrypt(data_bytes, self.key, self.timestamp)
            payload = encrypted_header + encrypted_data
            length = len(payload).to_bytes(4, byteorder='big')
            return length + payload

    @staticmethod
    def from_bytes(data: bytes, key: bytes) -> 'SPXMessage':
        """Deserialize from HDL."""
        if len(data) < 4:
            raise SPXProtocolError("Incomplete message")
        length = int.from_bytes(data[:4], byteorder='big')
        if len(data) < 4 + length:
            raise SPXProtocolError("Truncated message")
        payload = data[4:4+length]
        half = len(payload) // 2
        header_bytes = chrono_decrypt(payload[:half], key)
        data_bytes = chrono_decrypt(payload[half:], key)
        hdl = HolographicDataLattice()
        header = hdl.decode(header_bytes)
        data = hdl.decode(data_bytes)
        if merkle_forest_proof(header["id"]) != header["proof"]:
            raise SPXProtocolError("Merkle proof invalid")
        return SPXMessage(
            header["type"],
            header["id"],
            data,
            key,
            header["emotion"],
            header["intent"],
            header.get("error"),
            header["requires_ack"],
            header["swarm_key"]
        )

class SPXProtocolError(Exception):
    pass