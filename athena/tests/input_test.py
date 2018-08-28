"""
A simple test script to see if the brain is responding to input
"""
print('---- Running Input Test ----')

import traceback
import time

from athena import settings
from athena.brain import Brain

settings.USE_STT = False
settings.USE_TTS = False
my_brain = Brain(greet_user=False)

inputs = {
    'athena_control' : {
        'en-US' : [
            "list modules",
            "disable voice browse",
            "enable voice browse"
        ]
    },
    'conversation' : {
        'en-US' : [
            "why"
        ]
    },
    'geo_info' : {
        'en-US' : [
            "what city am I in",
            "what time is it",
            "what is my location"
        ]
    },
    'google' : {
        'en-US' : [
            "who is the president of america"
        ]
    },
    'hello_world' : {
        'en-US' : [
            "what kind of food should I eat tonight"
        ]
    },
    'music' : {
        'en-US' : [
            "play music"
        ]
    },
    'shop' : {
        'en-US' : [
            "order me a hundred biycle tires",
            "cancel my last bicycle tire order",
        ]
    },
    'sms_text' : {
        'en-US' : [
            "text my mom that I have rabies"
        ]
    },
    'twitter' : {
        'en-US' : [
            "post I just lost my lucky dolphin to twitter"
        ]
    },
    'uber' : {
        'en-US' : [
            "call a taxi for me",
            "cancel that last request"
        ]
    },
    'voice_browse' : {
        'en-US' : [
            "tell me about mushrooms",
            "close this browser"
        ]
    },
    'wolfram' : {
        'en-US' : [
            "How big is uranus"
        ]
    }
}

passed = True

try:
    for module, phrases in inputs.items():
        print("-------------------------------------")
        print("Testing {} module".format(module))
        print("-------------------------------------")
        for phrase in phrases[settings.LANG_4CODE]:
            print()
            print("Test phrase: '{}'".format(phrase))
            my_brain.match_mods(phrase)
            my_brain.execute_mods(phrase)
    print('---- TEST PASSED ----\n')
except:
    passed = False
    print(traceback.format_exc())

time.sleep(1)