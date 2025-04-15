# demo/legendary.py
# SPX Protocol legendary demo by Shaan (github.com/shaa2020)

import asyncio
import logging
from spx.client import SPXClient
from spx.server import SPXServer
from spx.protocol import SPXMessage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SPXLegendary")

async def run_legendary():
    server = SPXServer("localhost", 8443)
    client1 = SPXClient("localhost", 8443)
    client2 = SPXClient("localhost", 8443)
    server_task = asyncio.create_task(server.start())
    await asyncio.sleep(0.1)
    try:
        logger.info("🌌 The Cosmic Chat begins...")
        await client1.connect()
        await client2.connect()

        # Client 1 sends a message
        chat1 = SPXMessage.create_request(
            "CHAT",
            {"message": "Greetings from the stars!", "user": "Astra"},
            client1.key,
            emotion="joy",
            intent="create",
            requires_ack=True
        )
        logger.info("🌠 Astra sends: %s", chat1.data["message"])
        await client1.send_message(chat1)
        response1 = await client1.receive_message()
        logger.info("🌠 Astra receives: %s", response1.data["message"])

        # Client 2 responds
        chat2 = SPXMessage.create_request(
            "CHAT",
            {"message": "The cosmos replies!", "user": "Nebula"},
            client2.key,
            emotion="wonder",
            intent="explore",
            requires_ack=True
        )
        logger.info("🌠 Nebula sends: %s", chat2.data["message"])
        await client2.send_message(chat2)
        response2 = await client2.receive_message()
        logger.info("🌠 Nebula receives: %s", response2.data["message"])

        logger.info("🌌 The Cosmic Chat shines eternal. Visit github.com/shaa2020/spx-protocol!")
    finally:
        client1.close()
        client2.close()
        server_task.cancel()

if _name_ == "_main_":
    asyncio.run(run_legendary())