# spx/client.py
# SPX Protocol client by Shaan (github.com/shaa2020)

import asyncio
import logging
from typing import Optional
from .protocol import SPXMessage, SPXProtocolError
from .transport import NeuralStreamFabric
from .resilience import SymbioticSwarmIntelligence
from .crypto import ChronoCrypt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SPXClient")

class SPXClient:
    def _init_(self, host: str, port: int):
        self.host = host
        self.port = port
        self.transport = NeuralStreamFabric("0.0.0.0", 0)
        self.crypt = ChronoCrypt()
        self.key = self.crypt.generate_keypair("hope", "create")[1]
        self.ssi = SymbioticSwarmIntelligence()
        self.connected = False
        self.nodes = [(host, port)]

    async def connect(self):
        self.connected = True
        logger.info("🌌 Connected to %s:%s", self.host, self.port)
        asyncio.create_task(self.heartbeat())

    async def send_message(self, msg: SPXMessage):
        if not self.connected:
            raise SPXProtocolError("Not connected")
        start = time.time()
        await self.transport.send(msg.to_bytes(), self.key, (self.host, self.port), msg.msg_id)
        latency = time.time() - start
        if self.ssi.predict_failure(latency):
            new_node = self.ssi.evolve_route(msg.swarm_key)
            self.host, self.port = new_node.split(":")
            logger.warning("🌌 Evolved to %s", new_node)
        logger.debug("Sent: %s", msg.msg_type)
        if msg.requires_ack:
            ack = await self.receive_message()
            if ack.msg_type != f"{msg.msg_type}_ACK":
                raise SPXProtocolError("ACK failed")

    async def receive_message(self) -> SPXMessage:
        data, addr, stream_id = await self.transport.receive(self.key)
        msg = SPXMessage.from_bytes(data, self.key)
        logger.debug("Received: %s from %s", msg.msg_type, addr)
        return msg

    async def heartbeat(self):
        while self.connected:
            try:
                heartbeat = SPXMessage.create_request("HEARTBEAT", {}, self.key, emotion="calm", intent="protect")
                await self.send_message(heartbeat)
                await asyncio.sleep(30)
            except Exception as e:
                logger.error("Heartbeat failed: %s", e)
                self.connected = False
                await self.reconnect()

    async def reconnect(self):
        self.transport.close()
        self.transport = NeuralStreamFabric("0.0.0.0", 0)
        await self.connect()

    def close(self):
        self.transport.close()
        self.connected = False