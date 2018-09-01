"""
File Name: uber.py

This module demonstrates how you could call an uber

Usage Examples:
- "Order me an uber"
"""

from athena.classes.module import Module
from athena.classes.task import ActiveTask
from athena.mods import get_from_dict

ENABLED = True

class CallUberTask(ActiveTask):

    triggers = {
        'en-US' : [r"^\b(order|call|request)(?: me)? ((an |a )?(lyft|uber|taxi|limo)).*"],
        'is'    : [r"^\b(panta(?:ðu)?|hringdu á)(?: fyrir mig)? (leigubíl|taxa|úber|limósínu).*"]
    }
    
    response = {
        'en' : "Requesting {} for you.",
        'is' : "Græja {} fyrir þig.",
    }

    def __init__(self):
        # Matches any statement with these words
        super(CallUberTask, self).__init__(patterns=get_from_dict(self.triggers, ENABLED))

    def match(self, text):
        # Matches the 1 & 2 regex capture groups and stores them in variables
        return self.match_and_save_groups(text, {1: 'verb', 2: 'thing'})

    def action(self, text):
        return self.speak(get_from_dict(self.response, ENABLED, is_response=True).format(self.thing))


class CancelUberTask(ActiveTask):

    triggers = {
        'en-US' : [r".*\b(cancel.*(order|request|uber|lyft))\b.*"],
        'is'    : [r".*\b(hætt(?:a|u).*(pöntun(?:ina)?|leigubíl(?:inn)?|taxa(?:ann)?|úber(?:inn)?|limósínu(?:na)?))\b.*"]
    }
    
    response = {
        'en' : "Canceling ride sharing request.",
        'is' : "Hætti við pöntun."
    }

    def __init__(self):

        # Matches any statement with these words
        super(CancelUberTask, self).__init__(patterns=get_from_dict(self.triggers, ENABLED))

    def action(self, text):
        return self.speak(get_from_dict(self.response, ENABLED, is_response=True))


class CallUber(Module):

    def __init__(self):
        tasks = [CallUberTask(), CancelUberTask()]
        super(CallUber, self).__init__('uber', tasks, priority=2, enabled=ENABLED)
