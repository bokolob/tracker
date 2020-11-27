SETTINGS = {
              'apn': "internet.beeline.ru", 
              'login': "beeline",
              'password': "beeline",
              'send_sms_on_call': True,
              'sms_template': "http://www.google.com/maps/place/{lat},{lng}",
              'rtt_server': "5.9.136.109",
              'rtt_port': 3359,
              'min_bat_adc': 678,
              'max_bat_adc': 751,
              'bat_adc_scale': 95,
              'track_delay_minutes': 5,
              'locator_api_key':"AEsDOV8BAAAAelrSSQIAOzZ-PNLKVHQDKvFCBNbvhCGL7ZIAAAAAAAAAAABh6tFx3GfXVrXF72VITNRsa2otqQ==",
              'balance_ussd': "*102#",
              'admin_numbers':[],
              'admin_password':"",
              'disable_gprs_while_sleep': False,
              'disable_gps_while_sleep': False,

           }

def get_property(key):
    return SETTINGS[key]

def set_property(key, value):
    SETTINGS[key]=value

def load():
    raise ValueError("Not implemented")

def save():
    raise ValueError("Not Implemented")
