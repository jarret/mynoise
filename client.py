#!/usr/bin/env python3
import time
import asyncio
import coincurve



print("\nour static:")
our_static = bytes.fromhex(
    "1111111111111111111111111111111111111111111111111111111111111111")
s = coincurve.PrivateKey(secret=our_static)
print(s.to_hex())
print(s.public_key.format().hex())

print("\nour ephemeral:")
our_ephemeral = bytes.fromhex(
    "1212121212121212121212121212121212121212121212121212121212121212")
e = coincurve.PrivateKey(secret=our_ephemeral)
print("%066s" % e.to_hex())
print(e.public_key.format().hex())

print("\ntheir static:")
their_static = bytes.fromhex(
    "2121212121212121212121212121212121212121212121212121212121212121")

rs = coincurve.PrivateKey(secret=their_static)
print(rs.to_hex())
print(rs.public_key.format().hex())

a = s.ecdh(rs.public_key.public_key)
print("\necdh: %s" % a.hex())

class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, message, on_con_lost):
        self.message = message
        self.on_con_lost = on_con_lost

    def connection_made(self, transport):
        transport.write(self.message.encode())
        print('Data sent: {!r}'.format(self.message))

    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode()))

    def connection_lost(self, exc):
        print('The server closed the connection')
        self.on_con_lost.set_result(True)


async def main():
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    on_con_lost = loop.create_future()
    message = 'Hello World!'

    transport, protocol = await loop.create_connection(
        lambda: EchoClientProtocol(message, on_con_lost),
        '127.0.0.1', 8888)

    # Wait until the protocol signals that the connection
    # is lost and close the transport.
    try:
        await on_con_lost
    finally:
        transport.close()


asyncio.run(main())
