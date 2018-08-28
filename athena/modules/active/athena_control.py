"""
A module for controlling Athena

Usage Examples:
    - "Alfred stop"
    - "Enable Google"
"""

from athena.classes.module import Module
from athena.classes.task import ActiveTask
from athena import brain, log, mods


class QuitTask(ActiveTask):

    def __init__(self):
        super(QuitTask, self).__init__(patterns=[r'\b(alfred )?(quit|stop)\b.*'])

    def action(self, text):
        brain.inst.quit()


class ListModulesTask(ActiveTask):

    def __init__(self):
        super(ListModulesTask, self).__init__(words=['list modules', 'list mods'])

    def action(self, text):
        mods.list_mods()


class ToggleModuleTask(ActiveTask):

    def __init__(self):
        super(ToggleModuleTask, self).__init__(patterns=[r'.*\b(enable|add|disable|remove) (.*)'])
        self.groups = {1: 'enable', 2: 'module'}

    def match(self, text):
        return self.match_and_save_groups(text, self.groups)

    def action(self, text):
        mod_name = self.module.lower().strip().replace(' ', '')
        if 'disable' in self.enable.lower() or 'remove' in self.enable.lower():
            log.info("Attempting to disable '"+mod_name+"'")
            mods.disable_mod(mod_name)
        else:
            log.info("Attempting to enable '"+mod_name+"'")
            mods.enable_mod(mod_name)


class AthenaControl(Module):

    def __init__(self):
        tasks = [QuitTask(), ListModulesTask(), ToggleModuleTask()]
        super(AthenaControl, self).__init__('athena_control', tasks, priority=3)
