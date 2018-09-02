"""
    Allows users to send tweets via voice command

    Requires:
        - IFTTT configuration

    Usage Examples:
        - "Tweet What's up guys?"
        - "Post What's up everyone? to twitter"
"""

from athena.classes.module import Module
from athena.classes.task import ActiveTask
from athena.api_library import ifttt_api as ifttt
from athena.mods import get_from_dict

ENABLED = True

class SendTweetTask(ActiveTask):

    triggers = {
        'en-US' : [r'.*?\btweet (.+)',
                   r'.*\bpost (.+)\bto twitter\b',
                   r'.*\bpost to twitter\b(.+)'],
        'is'    : [r'.*?\btístaðu (.+)',
                   r'.*\bsettu (.+)\bá twitter\b',
                   r'.*\bsettu á twitter\b(.+)']
    }
    
    response = {
        'en' : "Sending tweet...",
        'is' : "Sendi tíst..."
    }

    def __init__(self):
        super(SendTweetTask, self).__init__(patterns=get_from_dict(self.triggers, ENABLED))

    def match(self, text):
        return self.match_and_save_groups(text, {1: 'tweet'})

    def action(self, text):
        print('\n~ Tweet: '+self.tweet)
        self.speak(get_from_dict(self.response, ENABLED, is_response=True), show_text=True)
        ifttt.trigger('voice_tweet', self.tweet)


class Twitter(Module):

    def __init__(self):
        tasks = [SendTweetTask()]
        super(Twitter, self).__init__('twitter', tasks, priority=3, enabled=ENABLED)
