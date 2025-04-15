
```MARKDOWN 
# Building a Cosmic Chat App with SPX

Create a secure, emotional chat app with SPX by Shaan ([github.com/shaa2020](https://github.com/shaa2020)).

## Prerequisites

```bash

pip install -r requirements.txt

```
Steps:

1. Run Server:

```bash
./run_server.sh
```
!. Create Client:

````PYTHON

# chat.py
import asyncio
from spx.client import SPXClient
from spx.protocol import SPXMessage

async def chat():
    client = SPXClient("localhost", 8443)
    await client.connect()
    msg = SPXMessage.create_request(
        "CHAT",
        {"message": "Hello, cosmos!", "user": "Star"},
        client.key,
        emotion="joy",
        intent="create"
    )
    await client.send_message(msg)
    response = await client.receive_message()
    print(f"🌌 {response.data['message']}")
    client.close()

asyncio.run(chat())
````

1. Run Client:

```bash
python chat.py
```