SETTINGS_PROTOTYPE = [
    {'key': 'send_sms_on_call', 'type': 'boolean', 'value': 'true'},
    {'key': 'sms_template', 'type': 'string', 'value': 'http://www.google.com/maps/place/{lat},{lng}'},
    {'key': 'admin_numbers', 'type': 'phone_list', 'value': ''},
    {'key': 'disable_gprs_while_sleep', 'type': 'boolean', 'value': 'true'},
    {'key': 'disable_gps_while_sleep', 'type': 'boolean', 'value': 'true'},
]


def settings_to_web_format(data):
    if data is None:
        return SETTINGS_PROTOTYPE

    result = []
    by_key = {x['key']: x for x in data}

    for row in SETTINGS_PROTOTYPE:
        value = by_key.get(row['key'], row).get('value')
        result.append({'key': row['key'], 'value': value, 'type': row['type']})

    return result


def settings_to_device_format(data):
    raise Exception('Not implemented')
