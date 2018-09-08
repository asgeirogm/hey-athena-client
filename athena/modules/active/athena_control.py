"""
A module for controlling Athena

Usage Examples:
    - "Alfred stop"
    - "Enable Google"
"""

from athena.classes.module import Module
from athena.classes.task import ActiveTask
from athena import brain, log, mods, settings
from athena.mods import get_from_dict

ENABLED = True

class QuitTask(ActiveTask):

    triggers = {
        'en-US' : [r'\b(alfred )?(quit|stop)\b.*'],
        'is'    : [r'\b(alfred )?stopp.*']
    }

    def __init__(self):
         super(QuitTask, self).__init__(patterns=get_from_dict(self.triggers, ENABLED))

    def action(self, text):
        brain.inst.quit()


class ListModulesTask(ActiveTask):

    triggers = {
        'en-US' : ['list modules', 'list mods'],
        'is' : ['.*lista(?:nn)? af einingum', 'sýndu mér einingarnar']
    }

    def __init__(self):
        super(ListModulesTask, self).__init__(words=get_from_dict(self.triggers, ENABLED))

    def action(self, text):
        mods.list_mods()


class ToggleModuleTask(ActiveTask):

    disable_triggers = {
        'en-US' : ['disable','remove'],
        'is'    : ['af(?:virkja|tengja)','fjarlægja']
    }

    triggers = {
        'en-US' : [r'.*\b(enable|add|{}) (.*)'.format('|'.join(get_from_dict(disable_triggers, ENABLED)))],
        'is'    : [r'.*\b(virkja|tengja|bæta við|{}) (.*)'.format('|'.join(get_from_dict(disable_triggers, ENABLED)))]
    }

    def __init__(self):
        super(ToggleModuleTask, self).__init__(patterns=get_from_dict(self.triggers, ENABLED))
        self.groups = {1: 'enable', 2: 'module'}

    def match(self, text):
        return self.match_and_save_groups(text, self.groups)

    def action(self, text):
        mod_name = self.module.lower().strip().replace(' ', '')
        
        should_disable = False
        for disable_trigger in get_from_dict(self.disable_triggers, ENABLED):
            if disable_trigger in self.enable.lower():
                should_disable = True
                break

        if should_disable:
            log.info("Attempting to disable '"+mod_name+"'")
            disable = mods.disable_mod(mod_name)
            self.speak(disable)
        else:
            log.info("Attempting to enable '"+mod_name+"'")
            enable = mods.enable_mod(mod_name)
            self.speak(enable)


class AthenaControl(Module):

    def __init__(self):
        tasks = [QuitTask(), ListModulesTask(), ToggleModuleTask()]
        super(AthenaControl, self).__init__('athena_control', tasks, priority=3, enabled=ENABLED)
