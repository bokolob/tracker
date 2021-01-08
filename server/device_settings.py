import model

SETTINGS_PROTOTYPE = [
    {'key': 'send_sms_on_call', 'type': 'boolean', 'value': 'true'},
    {'key': 'sms_template', 'type': 'string', 'value': 'http://www.google.com/maps/place/{lat},{lng}'},
    {'key': 'admin_numbers', 'type': 'phone_list', 'value': ''},
    {'key': 'disable_gprs_while_sleep', 'type': 'boolean', 'value': 'true'},
    {'key': 'disable_gps_while_sleep', 'type': 'boolean', 'value': 'true'},
]


def default_settings():
    buf = []
    for setting in SETTINGS_PROTOTYPE:
        buf.append(model.DeviceSettings(
            key=setting['key'],
            type=setting['type'],
            value=setting['value']))

    return buf


def convert_to_device_format(data):
    raise Exception('Not implemented')
