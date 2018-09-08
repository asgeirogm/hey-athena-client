"""
Wraps the Spotify Web Player to play music

Usage Examples:
    - "Open facebook.com"
    - "Search Neil Degrasse Tyson"
    - "Maximize the browser"
"""

from athena.classes.module import Module
from athena.classes.task import ActiveTask
from athena.apis import api_lib
from athena import log
from athena.mods import get_from_dict

ENABLED = True

class VoiceBrowseTask(ActiveTask):

    triggers = {
        'en-US' : [
            r'.*\b(?:search(?: for)?|look up|tell me about)\b(.*)',
            r'.*\b(?:go to|open)(.*\.(com|org|net|edu|gov|io|html))\b',
            r'.*\b(?:type)\b(.*)',
            r'.*\b(?:close|shut)(?: the| this)? (tab|page)\b.*',
            r'.*\b(?:close|shut)(?: the| this)? (browser)\b.*',
            r'.*\b(delete|clear the)\b.*',
            r'.*\b(maximize)\b.*',
            r'.*\b(click)\b.*',
            r'.*\b(?:next|switch the) (tab|page)\b.*'
        ],
        'is' : [
            r'.*\b(?:leita(?:ðu)?(?: að)?|flett(?:a|u) upp|segðu mér um)\b(.*)',
            r'.*\b(?:far(?:a|ðu) á|opna(?:ðu)?) (.*\.(com|org|net|edu|gov|io|html|is|dk))\b',
            r'.*\b(?:skrifa)(?:ðu)?\b(.*)',
            r'.*\b(?:loka(?:ðu)?)(?: þessum| þessari)? (flipa|glugga|síðu)\b.*',
            r'.*\b(?:loka(?:ðu)?)(?: þessum)? (vafra)(?:num)?\b.*',
            r'.*\b(eyða|eyddu|hreinsa(?:ðu)?|strokaðu(?:ðu)?(?: út)?)\b.*',
            r'.*\b(stækka(?:ðu)?)\b.*',
            r'.*\b(klikka(?:ðu)?)\b.*',
            r'.*\b(?:næst(?:a|u)|skiptu um) (flipa|glugga|síðu)\b.*'
        ]
    }

    def __init__(self):
        super(VoiceBrowseTask, self).__init__(patterns=get_from_dict(self.triggers, ENABLED))
        self.groups = {1: 'group1'}

    def match(self, text):
        return self.match_and_save_groups(text, self.groups)

    def action(self, text):
        try:
            api_lib['voice_browse_api'].driver.current_url
        except:
            api_lib['voice_browse_api'].driver = None
            log.debug('Browser was closed.')
        funcs = {
                 0: api_lib['voice_browse_api'].search,
                 1: api_lib['voice_browse_api'].open,
                 2: api_lib['voice_browse_api'].type,
                 3: api_lib['voice_browse_api'].close_tab,
                 4: api_lib['voice_browse_api'].close,
                 5: api_lib['voice_browse_api'].clear,
                 6: api_lib['voice_browse_api'].maximize,
                 7: api_lib['voice_browse_api'].click,
                 8: api_lib['voice_browse_api'].switch_tab,
        }
        if self.case < 3:
            funcs[self.case](self.group1)
        else:
            funcs[self.case]()


class VoiceBrowse(Module):

    def __init__(self):
        tasks = [VoiceBrowseTask()]
        super(VoiceBrowse, self).__init__('voice_browse', tasks, priority=2, enabled=ENABLED)
