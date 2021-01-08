import asyncio
import datetime
import os
import socket
from urllib.parse import urlparse

from aiomysql.sa import create_engine
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.sql import select

import model
from app import create_app

PROC_COUNT = 5
BULK_SIZE = 500
TIMEOUT = 2

queue = asyncio.Queue()
known_devices = dict()

app = create_app('')


def create_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', 25000))
    sock.listen()
    sock.setblocking(False)
    return sock


async def get_device_id(imei, engine):
    global known_devices
    if known_devices.get(imei) is not None:
        return known_devices.get(imei)

    statement = select([model.Device.id]).select_from(model.Device).where(model.Device.imei == imei).limit(1)

    async with engine.acquire() as conn:
        result_set = await conn.execute(statement)
        res = await result_set.fetchone()

        if res is not None:
            res = res.get("id")
            known_devices[imei] = res

        await result_set.close()

        return res


def get_id(device_id, timestamp=None):
    if timestamp is None:
        timestamp = datetime.datetime.now().timestamp();

    return (device_id << 32) | int(timestamp / 10) * 10


async def parse_input(line, engine):
    # print("XXXX " + str(line))
    proto, imei, timestamp, lat, lng, satelites, battery, status = line.split(b',')
    device_id = await get_device_id(imei.decode("latin1"), engine)
    return {'id': get_id(device_id, int(timestamp)),
            'device_id': device_id,
            'lat': lat.decode("latin1"),
            'lng': lng.decode("latin1")}


async def process_queue(engine):
    buf = []

    timeout = None

    while True:
        try:
            coords = await asyncio.wait_for(queue.get(), timeout=int(TIMEOUT / 2))
            buf.append(coords)
            queue.task_done()

            if timeout is None:
                timeout = datetime.datetime.now().timestamp() + TIMEOUT

        except asyncio.TimeoutError:
            pass

        if len(buf) >= BULK_SIZE or (
                len(buf) > 0 and timeout is not None and datetime.datetime.now().timestamp() >= timeout):
            async with engine.acquire() as conn:
                trans = await conn.begin()

                act = insert(model.Coordinates).values(buf)

                on_duplicate_key_stmt = act.on_duplicate_key_update(
                    {'lat': act.inserted.lat, 'lng': act.inserted.lng}
                )

                await conn.execute(on_duplicate_key_stmt)
                await trans.commit()

            timeout = None

            buf = []


async def handler(event_loop, client, engine):
    print("handler" + str(os.getpid()))
    with client:
        buf = bytearray()

        while True:
            try:
                data = await asyncio.wait_for(event_loop.sock_recv(client, 64), timeout=5)

                if not data:
                    break
                else:
                    buf += data
                    if b'\n' in buf:
                        coords = await parse_input(buf, engine)
                        await queue.put(coords)

                        print(coords)

            except asyncio.TimeoutError:
                print("timeout")
                break


async def server_loop(loop, server_sock):
    mysql_params = urlparse(app.config['SQLALCHEMY_DATABASE_URI'])
    engine = await create_engine(user=mysql_params.username, db=mysql_params.path.strip("/"),
                                 host=mysql_params.hostname, password=mysql_params.password, loop=loop)

    loop.create_task(process_queue(engine))

    while True:
        (conn, address) = await loop.sock_accept(server_sock)
        loop.create_task(handler(loop, conn, engine))


server_sock = create_server()

# for num in range(PROC_COUNT):
#    pid = os.fork()
#    if pid <= 0:
#        break

loop = asyncio.get_event_loop()
loop.create_task(server_loop(loop, server_sock))
loop.run_forever()
