import socket
from datetime import datetime
from math import sqrt
from os import listdir
from os.path import isfile, join
from time import sleep

import gpxpy
import gpxpy.gpx

SPEED = 0.0003


def get_point(gpx):
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                yield point


def distance(p1, p2):
    return sqrt((p1.latitude - p2.latitude) ** 2 + (p1.longitude - p2.longitude) ** 2)


def send_coords(lat, long, timestamp):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", 25000))
    # proto, imei, timestamp, lat, lng, satelites, battery, status = line.split(b',')
    sock.send(
        bytearray("1,deadbeef," + str(timestamp) + "," + str(lat) + "," + str(long) + ",sat,battery,ok\n", "latin1"))
    sock.close()


files = [join('./gpx_examples', f) for f in listdir('./gpx_examples') if isfile(join('./gpx_examples', f))]

for file in files[6:7]:
    gpx_file = open(file, 'r')
    gpx = gpxpy.parse(gpx_file)

    iterator = get_point(gpx)
   # timestamp = int(datetime.now().timestamp())

    first = next(iterator)

    while True:
        try:
            next_point = next(iterator)
        except StopIteration:
            break

        dist = distance(first, next_point)

        if dist == 0.0:
            first = next_point
            continue

        unit_vector = [(next_point.latitude - first.latitude) / dist, (next_point.longitude - first.longitude) / dist]

        progress = 0.0

        position = [0.0, 0.0]

        while progress < dist:
            position[0] = first.latitude + unit_vector[0] * progress
            position[1] = first.longitude + unit_vector[1] * progress
            print('Point at ({0},{1})'.format(position[0], position[1]))

            send_coords(position[0], position[1], int(datetime.now().timestamp()))

            progress = progress + SPEED
            sleep(1)
            #timestamp = timestamp + 10

        first = next_point
