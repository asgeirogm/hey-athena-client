"""
A tool for retrieving geographical info based on external IP
| API Documentation: http://ip-api.com
"""

import requests

from time import strftime
from athena.mods import get_from_dict
from athena import settings

URL = 'http://ip-api.com/json'

response = None


def update_data():
    """ Update the location data cache """
    global response
    response = requests.get(URL).json()


def location():
    loc = get_data('city')+', '+get_data('regionName')
    return loc.title()


def time():
    if settings.TIME_FORMAT == 12:
        return strftime('%I:%M %p').lstrip('0')
    elif settings.TIME_FORMAT == 24:
        return strftime('%H:%M').lstrip('0')


def get_data(key):
    """ Returns the desired data given an input key """
    """
    Keys/Values:
        | status: SUCCESS,
        | country: COUNTRY,
        | countryCode: COUNTRY CODE,
        | region: REGION CODE,
        | regionName: REGION NAME,
        | city: CITY,
        | zip: ZIP CODE,
        | lat: LATITUDE,
        | lon: LONGITUDE,
        | timezone: TIME ZONE,
        | isp: ISP NAME,
        | org: ORGANIZATION NAME,
        | as: AS NUMBER / NAME,
        | query: IP ADDRESS USED FOR QUERY
    """
    aliases = {
        'en-US' : {
            'state':        'regionName',
            'zip code':     'zip',
            'latitude':     'lat',
            'longitude':    'lon',
            'internet service provider': 'isp',
            'ip':           'query'
        },
        'is' : {
            'svæði':        'regionName',
            'póstnúmer':    'zip',
            'hæðargráðu':   'lat',
            'lengdargráðu': 'lon',
            'símafyrirtæki':'isp',
            'ip':           'query',
            'borg':         'city'
        }
    }  # Spoken words mapped to actual keys
    
    location_triggers = { 
        'en-US' : ['where', 'location'],
        'is'    : ['hvar', 'staðsetning']
    }
    
    if key in get_from_dict(aliases):
        key = get_from_dict(aliases)[key]
    
    for location_trigger in get_from_dict(location_triggers):
        if location_trigger in key.lower():
            return location()

    if key not in response:
        return None
    return response[key]
