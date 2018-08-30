"""
Uses the external IP to find geographical info

Usage Examples:
    - "What time is it?"
    - "Where am I?"
"""

from athena.classes.module import Module
from athena.classes.task import ActiveTask
from athena.api_library import geo_info_api
from athena.mods import get_from_dict

ENABLED = True

class GetIPInfoTask(ActiveTask):

    triggers = {
        'en-US' : ['ip', 'country', 'region', 'city', 'latitude',
                   'longitude', 'isp', 'internet service provider',
                   'timezone', 'time', 'where am I', 'where are we',
                   'location']
    }
    
    response = {
        'en' : "It\'s currently {}",
    }

    def __init__(self):
        super(GetIPInfoTask, self).__init__(words=get_from_dict(self.triggers, ENABLED))

        # geo_info_api.update_data()
        self.groups = {1: 'query'}

    def match(self, text):
        return self.match_and_save_groups(text, self.groups)

    def action(self, text):
        if 'time' in self.query:
            self.speak(get_from_dict(self.response, ENABLED, is_response=True).format(geo_info_api.time())) 
            return

        geo_info_api.update_data()
        self.speak(str(geo_info_api.get_data(self.query)))


class GeoInfo(Module):

    def __init__(self):
        tasks = [GetIPInfoTask()]
        super(GeoInfo, self).__init__('geo_info', tasks, priority=3, enabled=ENABLED)
