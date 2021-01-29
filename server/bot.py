import getopt
import socket
import sys
from datetime import datetime
from math import sqrt
from os import listdir
from os.path import isfile, join
from time import sleep

import gpxpy.gpx

SPEED = 0.0003

imei = ""


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
        bytearray("1," + imei + "," + str(timestamp) + "," + str(lat) + "," + str(long) + ",sat,battery,ok\n",
                  "latin1"))
    sock.close()


def process_file(path):
    gpx_file = open(path, 'r')
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
            # timestamp = timestamp + 10

        first = next_point


def main():
    global imei
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i=f=", ["imei=", "file="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        # TODO usage()
        sys.exit(2)

    file = 0

    for o, a in opts:
        if o in ("-i", "--imei"):
            imei = a
        elif o in ("-f", "--file"):
            file = a
        else:
            assert False, "unhandled option"

    files = sorted([join('./gpx_examples', f) for f in listdir('./gpx_examples') if isfile(join('./gpx_examples', f))])
    process_file(files[int(file)])


if __name__ == "__main__":
    main()
