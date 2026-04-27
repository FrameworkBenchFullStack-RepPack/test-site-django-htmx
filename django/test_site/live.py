import asyncio
import threading
import time

LIVE_DATA = [
    [48, 32, 75],
    [53, 38, 69],
    [59, 44, 62],
    [65, 49, 56],
    [70, 55, 50],
    [75, 61, 44],
    [80, 66, 38],
    [85, 71, 33],
    [88, 75, 27],
    [91, 78, 22],
    [92, 80, 20],
    [90, 77, 25],
    [86, 73, 30],
    [83, 68, 35],
    [78, 63, 41],
    [73, 58, 47],
    [67, 52, 53],
    [62, 47, 59],
    [56, 41, 65],
    [51, 35, 72],
]

async_clients = []
live_index = 0
_broadcast_started = threading.Event()


def _broadcast_loop():
    global live_index
    while True:
        data = LIVE_DATA[live_index]
        payload = (
            f"event: data-1\ndata: {data[0]}\n\n"
            f"event: data-2\ndata: {data[1]}\n\n"
            f"event: data-3\ndata: {data[2]}\n\n"
        )

        live_index = (live_index + 1) % len(LIVE_DATA)

        for queue in async_clients:
            try:
                queue.put_nowait(payload)
            except asyncio.QueueFull:
                pass

        time.sleep(1)


def start_live_broadcast():
    if not _broadcast_started.is_set():
        _broadcast_started.set()
        thread = threading.Thread(target=_broadcast_loop, daemon=True)
        thread.start()


async def live_broadcast_async():
    start_live_broadcast()
