# tests/test_transport.py
# SPX Protocol NSF tests by Shaan (github.com/shaa2020)

import unittest
import asyncio
from spx.transport import NeuralStreamFabric

class TestNSF(unittest.TestCase):
    async def test_send(self):
        nsf = NeuralStreamFabric("localhost", 0)
        await nsf.send(b"test", b"key", ("localhost", 8443), "stream1")
        nsf.close()

    def test(self):
        asyncio.run(self.test_send())