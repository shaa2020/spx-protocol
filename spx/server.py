# spx/server.py
# SPX Protocol server by Shaan (github.com/shaa2020)

import asyncio
import logging
from typing import Dict
from .protocol import SPXMessage, SPXProtocolError
from .transport import NeuralStreamFabric
from .resilience import SymbioticSwarmIntelligence
from .generative import GenerativeProtocolExtension

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SPXServer")

class SPXServer:
    def _init_(self, host: str, port: int):
        self.host = host
        self.port = port
        self.transport = NeuralStreamFabric(host, port)
        self.ssi = SymbioticSwarmIntelligence()
        self.gpe = GenerativeProtocolExtension()
        self.key = b"serverkey"
        self.handlers = {
            "PING": self.handle_ping,
            "HEARTBEAT": self.handle_heartbeat,
            "CHAT": self.handle_chat
        }

    async def start(self):
        logger.info("🌌 SPX Server ignites on %s:%s", self.host, self.port)
        while True:
            data, addr, stream_id = await self.transport.receive(self.key)
            try:
                msg = SPXMessage.from_bytes(data, self.key)
                logger.debug("Received: %s from %s", msg.msg_type, addr)
                if not self.ssi.predict_failure(time.time()):
                    response = await self.process_message(msg)
                    await self.transport.send(response.to_bytes(), self.key, addr, stream_id)
                    if msg.requires_ack:
                        ack = SPXMessage.create_response(msg, {}, self.key)
                        ack.msg_type = f"{msg.msg_type}_ACK"
                        await self.transport.send(ack.to_bytes(), self.key, addr, stream_id)
            except SPXProtocolError as e:
                logger.error("Error: %s", e)

    async def process_message(self, msg: SPXMessage) -> SPXMessage:
        handler = self.handlers.get(msg.msg_type, self.gpe.suggest_handler(msg.msg_type))
        return await handler(msg)

    async def handle_ping(self, msg: SPXMessage) -> SPXMessage:
        return SPXMessage.create_response(msg, {"status": "ok", "value": msg.data.get("value")}, msg.key)

    async def handle_heartbeat(self, msg: SPXMessage) -> SPXMessage:
        return SPXMessage.create_response(msg, {}, msg.key)

    async def handle_chat(self, msg: SPXMessage) -> SPXMessage:
        return SPXMessage.create_response(msg, {"message": f"Echo: {msg.data.get('message')}"}, msg.key)

if _name_ == "_main_":
    server = SPXServer("localhost", 8443)
    asyncio.run(server.start())