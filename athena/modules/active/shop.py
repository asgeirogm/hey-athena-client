"""
File Name: hello_world.py
Shop with your voice
Usage Examples:
- "Order me some pizza"
"""

from athena.classes.module import Module
from athena.classes.task import ActiveTask
from athena.mods import get_from_dict
ENABLED = True

class OrderSomething(ActiveTask):

    triggers = {
        'en-US' : [r'^\b(order|buy)(?: me)?\b(.*)']
    }
    
    response_replacements = {
        'en' : {
            "my" : "your",
            "favor" : "Favor"
        }
    }

    response = {
        'en' : "Getting you {}."
    }

    def __init__(self):
        # Matches any statement with these words
        super(OrderSomething, self).__init__(patterns=get_from_dict(self.triggers, ENABLED))

    def match(self, text):
        return self.match_and_save_groups(text, {1: 'verb', 2: 'thing'})

    def action(self, text):
        for target, replacement in get_from_dict(self.response_replacements, ENABLED, is_response=True).items():
            self.thing = self.thing.replace(target, replacement)

        return ('shop', get_from_dict(self.response, ENABLED, is_response=True).format(self.thing))


class CancelOrder(ActiveTask):
    
    triggers = {
        'en-US' : [r'.*\b(cancel.*order)\b.*']
    }

    response = {
        'en' : "Canceling previous order."
    }

    def __init__(self):
        # Matches any statement with these words
        super(CancelOrder, self).__init__(patterns=get_from_dict(self.triggers, ENABLED))

    def action(self, text):
        return ('shop', get_from_dict(self.response, ENABLED, is_response=True))


class Shop(Module):

    def __init__(self):
        tasks = [OrderSomething(), CancelOrder()]
        super(Shop, self).__init__('shop', tasks, priority=2, enabled=ENABLED)
