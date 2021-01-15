import socket

import gps
import ujson

import gprs
import urequests
from settings import get_property

gps_state = False


def set_gps_state(state):
    global gps_state

    prev_state = gps_state;

    if state and (not gps_state):
        gps.on(0, 1 | 2)
    else:
        if not state and gps_state:
            print("Switchng off gps!")
            gps.off()

    gps_state = state;
    return prev_state


def prepare_yndx_locator_request():
    gps_data = cellular.agps_station_data()

    mcc = gps_data[0]
    mnc = int(gps_data[1] / 10)
    stations = gps_data[2]

    gsm_cells = [{"countrycode": mcc,
                  "operatorid": mnc,
                  "lac": x[0],
                  "cellid": x[1],
                  "signal_strength": x[2],
                  } for x in stations
                 ]

    return {
        "common": {
            "version": "1.0",
            "api_key": get_property('locator_api_key'),
        },
        "gsm_cells": gsm_cells,
        "ip": {
            "address_v4": None
        }
    }


def get_lbs_location():
    gprs.wait_gprs()
    req = prepare_yndx_locator_request()
    req["ip"]["address_v4"] = socket.get_local_ip()

    coords = (0, 0, False)
    resp = None

    try:
        resp = urequests.post("http://api.lbs.yandex.net/geolocation",
                              data="json=" + ujson.dumps(req),
                              headers={"Content-Type": "application/x-www-form-urlencoded", "Accept": "*/*"})

        if resp.status_code == 200:
            parsed = resp.json()
            coords = (parsed['position']['latitude'], parsed['position']['longitude'], False)
    finally:
        if resp != None:
            resp.close()

    return coords


def has_gps_fix():
    nmea = gps.nmea_data()
    return nmea != None and len(nmea) >= 2 and nmea[0][1] and len(nmea[1]) > 0 and nmea[1][0][1] > 1


def get_coordinates():
    global gps_state

    if gps_state and has_gps_fix():
        coords = gps.get_location()
        return (coords[0], coords[1], True)

    return get_lbs_location()
