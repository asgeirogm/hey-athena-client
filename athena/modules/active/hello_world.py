"""
        File Name: hello_world.py
        Tells you what to eat
        Usage Examples:
        - "What type of food should I eat tonight"
"""

from athena.classes.module import Module
from athena.classes.task import ActiveTask
from athena.mods import get_from_dict

ENABLED = True

class SpeakPhrase(ActiveTask):

    triggers = {
        'en-US' : ['eat', 'food', 'type']
    }

    def __init__(self):
        # Matches any statement with these words
        super(SpeakPhrase, self).__init__(words=get_from_dict(self.triggers, ENABLED))

    def action(self, text):
        self.speak('You should eat Mexican food tonight')


# This is a bare-minimum module
class HelloWorld(Module):

    def __init__(self):
        tasks = [SpeakPhrase()]
        super(HelloWorld, self).__init__('hello_world', tasks, priority=2, enabled=ENABLED)
