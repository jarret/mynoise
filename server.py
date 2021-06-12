#!/usr/bin/env python3
import time
import asyncio


print("\nour static:")
our_static = bytes.fromhex(
    "2121212121212121212121212121212121212121212121212121212121212121")
print("\nour ephemeral:")
our_ephemeral = bytes.fromhex(
    "2222222222222222222222222222222222222222222222222222222222222222")
print("\ntheir static:")
their_static = bytes.fromhex(
    "1111111111111111111111111111111111111111111111111111111111111111")

class EchoServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        print('Data received: {!r}'.format(message))

        print('Send: {!r}'.format(message))
        self.transport.write(data)

        print('Close the client socket')
        self.transport.close()


async def main():
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    server = await loop.create_server(
        lambda: EchoServerProtocol(),
        '127.0.0.1', 8888)

    async with server:
        await server.serve_forever()


asyncio.run(main())
