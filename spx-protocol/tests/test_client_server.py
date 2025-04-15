# tests/test_client_server.py
# SPX Protocol integration tests by Shaan (github.com/shaa2020)

import unittest
import asyncio
from spx.client import SPXClient
from spx.server import SPXServer

class TestClientServer(unittest.TestCase):
    async def test_chat(self):
        server = SPXServer("localhost", 8443)
        client = SPXClient("localhost", 8443)
        server_task = asyncio.create_task(server.start())
        await asyncio.sleep(0.1)
        await client.connect()
        msg = SPXMessage.create_request("CHAT", {"message": "test"}, client.key, emotion="hope", intent="create")
        await client.send_message(msg)
        response = await client.receive_message()
        self.assertEqual(response.msg_type, "CHAT_RESP")
        client.close()
        server_task.cancel()

    def test(self):
        asyncio.run(self.test_chat())