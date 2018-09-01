"""
A simple test script to see if the brain is responding to input
"""
print('---- Running Input Test ----')

import traceback
import time
import argparse

from athena import settings, mods
from athena.brain import Brain

INPUTS = {
        'athena_control' : {
            'en-US' : [
                "list modules",
                "disable voice browse",
                "enable voice browse"
            ],
            'is' : [
                "lista af einingum",
                "afvirkja voice browse",
                "virkja voice browse"
            ]
        },
        'conversation' : {
            'en-US' : [
                "why"
            ],
            'is' : [
                "sesdfgðu mér sdfsdbrandara"
            ]
        },
        'geo_info' : {
            'en-US' : [
                "what city am I in",
                "what time is it",
                "what is my location"
            ],
            'is' : [
                "Í hvaða borg er ég",
                "hvað er klukkan",
                "hver er mín staðsetning"
            ]
        },
        'google' : {
            'en-US' : [
                "who is the president of america"
            ],
            'is' : [
                "hver er forseti bandaríkjanna"
            ]
        },
        'hello_world' : {
            'en-US' : [
                "what kind of food should I eat tonight"
            ],
            'is' : [
                "hvernig mat á ég að borða í kvöld"
            ]
        },
        'music' : {
            'en-US' : [
                "play music"
            ],
            'is' : [
                "spila tónlist"
            ]
        },
        'shop' : {
            'en-US' : [
                "order me a hundred biycle tires",
                "cancel my last bicycle tire order",
            ],
            'is' : [
                "pantaðu handa mér hundrað dekk undir hjól",
                "hætta við síðustu pöntunina mína",
            ]
        },
        'sms_text' : {
            'en-US' : [
                "text my mom that I have rabies"
            ],
            'is' : [
                "sendu sms á mömmu um að ég sé með hundaæði"
            ]
        },
        'twitter' : {
            'en-US' : [
                "post I just lost my lucky dolphin to twitter"
            ],
            'is' : [
                "settu ég er nýbúinn að týna happa höfrungnum mínum á twitter"
            ]
        },
        'uber' : {
            'en-US' : [
                "call a taxi for me",
                "cancel that last request"
            ],
            'is' : [
                "hringdu á leigubíl fyrir mig",
                "hættu við leigubílinn"
            ]
        },
        'voice_browse' : {
            'en-US' : [
                "tell me about mushrooms",
                "close this browser"
            ],
            'is' : [
                "segðu mér um sveppi",
                "lokaðu þessum vafra"
            ]
        },
        'wolfram' : {
            'en-US' : [
                "How big is uranus"
            ],
            'is' : [
                "Hversu stór er Úranus"
            ]
        }
    }

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-s', '--speech-language',
                        dest='speech_language',
                        default=settings.LANG_4CODE,
                        help='Specify a language on LCID format (see settings.py for help). Defaults to settings.LANG_4CODE.')
    parser.add_argument('-r', '--response-language',
                        dest='response_language',
                        default=settings.LANG_CODE,
                        help='Specify a language in two characer format (see settings.py for help). Defaults to settings.LANG_CODE.')
    args = parser.parse_args()
    
    settings.LANG_4CODE = args.speech_language
    settings.LANG_CODE = args.response_language
    
    settings.USE_STT = False
    settings.USE_TTS = False
    my_brain = Brain(greet_user=False)
    
    passed = True

    try:
        for mod in mods.mod_lib:
            if mod.name in INPUTS:
                phrases = INPUTS[mod.name]
                print("-------------------------------------")
                print("Testing {} module".format(mod.name))
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

if __name__ == '__main__':
    main()
    