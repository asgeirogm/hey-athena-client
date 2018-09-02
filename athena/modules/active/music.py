"""
A simple module for playing music

Usage Examples:
    - "Play some music"
    - "Turn up!"
"""

from athena.classes.module import Module
from athena.classes.task import ActiveTask
from athena.tts import play_mp3
from athena.mods import get_from_dict

# Checks 'media' folder by default
TURN_UP_SONG = 'godj.wav'

ENABLED = True

class PlaySongTask(ActiveTask):
        
    triggers = {
        'en-US' : [r'.*\b(get turnt|turn up|play.*music)\b.*'],
        'is'    : [r'.*\b(spila.*tónlist)\b.*'],
    }
    
    response = {
        'en' : "Turning up...",
        'is' : "Skelli ljúfum tónum á fóninn...",
    }

    def __init__(self):
        super(PlaySongTask, self).__init__(patterns=get_from_dict(self.triggers, ENABLED))

    def action(self, text):
        self.speak(get_from_dict(self.response, ENABLED, is_response=True))
        play_mp3(TURN_UP_SONG)


class Music(Module):

    def __init__(self):
        tasks = [PlaySongTask()]
        super(Music, self).__init__('music', tasks, priority=2, enabled=ENABLED)
