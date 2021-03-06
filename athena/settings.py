"""
Global settings are stored here
"""

import logging
import sys
import speech_recognition as sr

from os import mkdir, path
from os.path import join
from sys import platform as _platform

from athena import api_library
from athena.modules import active as active_mods

# Wake-up Word(s) must be in the sphinx dict file (or else RuntimeError occurs)
# Change to 'hey athena' if background noise triggering occurs
WAKE_UP_WORD = "alfred"

# (not implemented yet) active listen until no input is received (for conversation)
FREQUENT_ACTIVE_LISTEN = True

# Current choices: ["google", "sphinx"]
# NOTE: only english is supported for sphinx by default at the time
ACTIVE_ENGINE = "google"

# Set these to False while debugging
USE_STT = True
USE_TTS = True

# Max gTTS (speaking) string length
MAX_CHAR = 140


"""
LANGS = ['af', 'sq', 'ar', 'hy', 'ca', 'zh-CN', 'zh-TW', 'hr', 'cs',
         'da', 'nl', 'en', 'eo', 'fi', 'fr', 'de', 'el', 'ht', 'hi',
         'hu', 'is', 'id', 'it', 'ja', 'ko', 'la', 'lv', 'mk', 'no',
         'pl', 'pt', 'ro', 'ru', 'sr', 'sk', 'es', 'sw', 'sv', 'ta',
         'th', 'tr', 'vi', 'cy']
"""
# Lang Code/LCID reference: http://www.science.co.il/language/Locale-codes.php
# NOTE: Changing this only changes STT & TTS (not module pattern matching)
LANG_CODE = 'is'
LANG_4CODE = 'is'  # LCID String

# Time format for output. Choices are [12, 24] 
TIME_FORMAT = 24

#####################
#    DIRECTORIES    #
#####################
CLIENT_DIR =    path.dirname(path.abspath(__file__))
BASE_DIR =      path.dirname(CLIENT_DIR)
DATA_DIR =      path.join(CLIENT_DIR, 'data')
LOGS_DIR =      path.join(DATA_DIR,   'logs')
MEDIA_DIR =     path.join(DATA_DIR,   'media')
INPUTS_DIR =    path.join(MEDIA_DIR,  'example_inputs')
RESPONSES_DIR = path.join(MEDIA_DIR,  'responses')
USERS_DIR =     path.join(DATA_DIR,   'users')

LOG_NAME = 'athena'
LOG_FILE = path.join(LOGS_DIR, LOG_NAME+'.log')
LOG_LEVEL = logging.DEBUG


CHROME_DRIVER = path.join(CLIENT_DIR, 'chrome', 'win32', 'chromedriver.exe')
if _platform.startswith("linux"):
    CHROME_DRIVER = path.join(CLIENT_DIR, 'chrome', 'linux32', 'chromedriver')
elif _platform == "darwin":
    CHROME_DRIVER = path.join(CLIENT_DIR, 'chrome', 'mac64', 'chromedriver')


API_DIRS = [
    # Add your custom api directory strings here (e.g. - "C:/my_custom_api_dir")
]
API_DIRS.extend(api_library.__path__)
MOD_DIRS = [
    # Add your custom api directory strings here (e.g. - "C:/my_custom_mod_dir")
]
MOD_DIRS.extend(active_mods.__path__)

# Get speech_recognition pocketsphinx models
SR_DIR = path.dirname(path.abspath(sr.__file__))
MODEL_DIR = path.join(SR_DIR, 'pocketsphinx-data')

DIRS = [LOGS_DIR, MEDIA_DIR, INPUTS_DIR, RESPONSES_DIR, USERS_DIR]

for d in DIRS:
    if not path.exists(d):
        mkdir(d)

POCKETSPHINX_LOG = join(LOGS_DIR,   'passive-listen.log')
ACOUSTIC_MODEL =   join(MODEL_DIR,  'en-US', 'acoustic-model')
LANGUAGE_MODEL =   join(MODEL_DIR,  'en-US', 'language-model.lm.bin')
POCKET_DICT =      join(MODEL_DIR,  'en-US', 'pronounciation-dictionary.dict')
KEYPHRASES =       join(CLIENT_DIR, 'keyphrases.txt')
# For custom word pronounciations, edit the pocketsphinx dictionary above

#####################
#     RESPONSES     #
#####################
RESPONSES = {
    'en' : {
        'error'      : "Something went wrong. Would you like to see the error message?",
        'no_modules' : "I'm not sure how to respond to that.",
        'no_mic'     : "I couldn't connect to a microphone."
    },
    'is' : {
        'error'      : "Eitthvað fór úrskeiðis. Viltu sjá villuskilaboðin?",
        'no_modules' : "Ég náði þessu ekki alveg hjá þér.",
        'no_mic'     : "Hljóðnemi finnst ekki."
    }
}
ERROR =      RESPONSES[LANG_CODE]['error']
NO_MODULES = RESPONSES[LANG_CODE]['no_modules']
NO_MIC =     RESPONSES[LANG_CODE]['no_mic']

#####################
#     FREE KEYS     #
#####################
WOLFRAM_KEY =      '4QR84U-VY7T7AVA34'
WUNDERGROUND_KEY = 'd647ca403a0ac94b'
IFTTT_KEY =        ''

CONTACTS = {}

#####################
#   BASIC REGEX     #
#####################
PHONE_REGEX = r"\b((\(\d{3}\)|\d{3})-?\d{3}-?\d{4})\s?(.*)"