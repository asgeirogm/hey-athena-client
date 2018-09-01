"""
DISABLED by default (since this module can be buggy)

Handles most general questions (including math!)

Usage Examples:
    - "How tall is Mount Everest?"
"""

from googletrans import Translator

from athena.classes.module import Module
from athena.classes.task import ActiveTask
from athena.apis import api_lib
from athena import log, settings
from athena.mods import get_from_dict

ENABLED = False

class AnswerTask(ActiveTask):

    triggers = {
        'en-US' : [r".*\b((who|what|when|where|why|how)(\')?(s)?|" +
                  r"(can|are|is|will|define|show me|say))\b.*"],
        'is'    : [r".*\b((hver|hvað|hvenær|hvar|afhverju|hvernig)(\')?(s)?|" +
                  r"(getur|gat|eru|er|verður|skilgreindu|sýndu mér|segðu))\b.*"]
    }

    def __init__(self):
        super(AnswerTask, self).__init__(patterns=get_from_dict(self.triggers, ENABLED))

    def action(self, text):
        translator = Translator()
        speech_language = settings.LANG_4CODE[:2].lower()
        if speech_language != 'en':
            log.info('\n~ Translating to english\n')
            translation = translator.translate(text, src=speech_language, dest='en')
            text = translation.text
        log.info('\n~ Searching Google...\n')
        api_lib['voice_browse_api'].search(text)


class Google(Module):

    def __init__(self):
        tasks = [AnswerTask()]
        super(Google, self).__init__('google', tasks, priority=1, enabled=ENABLED)
