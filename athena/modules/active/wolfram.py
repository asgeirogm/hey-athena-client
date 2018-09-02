"""
Handles most general questions (including math!)

Requires:
    - WolframAlpha API key

Usage Examples:
    - "How tall is Mount Everest?"
    - "What is the derivative of y = 2x?"
"""

import wolframalpha
from googletrans import Translator

from athena.classes.module import Module
from athena.classes.task import ActiveTask
from athena import log, settings

wolfram_client = wolframalpha.Client(settings.WOLFRAM_KEY)

class AnswerTask(ActiveTask):

    translator = Translator()

    def match(self, text):
        return True

    def action(self, text):
        speech_language = settings.LANG_4CODE[:2].lower()
        if speech_language != 'en':
            log.info('\n~ Translating to english\n')
            translation = self.translator.translate(text, src=speech_language, dest='en')
            text = translation.text
        try:
            query = wolfram_client.query(text)
            response_language = settings.LANG_CODE.lower()
            answer = next(query.results).text
            if speech_language != 'en':
                log.info('\n~ Translating to response language {}\n'.format(response_language))
                translation = self.translator.translate(answer, src='en', dest=response_language)
                answer = translation.text
            self.speak(answer)
        except:
            self.speak(settings.NO_MODULES)


class Wolfram(Module):

    def __init__(self):
        tasks = [AnswerTask()]
        super(Wolfram, self).__init__('wolfram', tasks, priority=0)
