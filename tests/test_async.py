import sys
sys.path.append('/workspace')
from pyee import *
import time
import asyncio
from pyee.asyncio import AsyncIOEventEmitter
from asyncio import sleep

ee_async = AsyncIOEventEmitter()

@ee_async.on("event")
async def event_handler():
    print("BANG BANG")
    await sleep(1)
    print("I'm done")

async def async_task():
    for i in range(5):
        print(f'Emitted event {i} at {time.time()}')
        ee_async.emit("event")
        await sleep(2)
    print(f'Emitted event and cancel at {time.time()}')
    ee_async.emit("event")
    await sleep(0.5)
    ee_async.cancel()
    print(f'Emitted event after cancel at {time.time()}')
    ee_async.emit("event")

async def background_task():
    print(f'Background task started at {time.time()}')
    await sleep(15)
    print(f'Background task ended at {time.time()}')

async def main():
    await asyncio.gather(
        async_task(),
        background_task()
    )

asyncio.run(main())