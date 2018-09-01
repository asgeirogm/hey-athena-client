"""
Finds and stores APIs in the 'api_lib' global variable
"""

import pkgutil
import inspect
import traceback

from athena import settings, log

mod_lib = None


def find_mods():
    """ Find and import modules from the module directories """
    global mod_lib
    mod_lib = []
    log.debug('Looking for modules in: '+str(settings.MOD_DIRS))
    for finder, name, _ in pkgutil.iter_modules(settings.MOD_DIRS):
        try:
            mod = finder.find_module(name).load_module(name)
            for member in dir(mod):
                obj = getattr(mod, member)
                if inspect.isclass(obj):
                    for parent in obj.__bases__:
                        if 'Module' is parent.__name__:
                            if obj().enabled:
                                mod_lib.append(obj())
        except Exception as e:
            print(traceback.format_exc())
            log.error('Error loading \''+name+'\' '+str(e))
    mod_lib.sort(key=lambda mod: mod.priority, reverse=True)


def list_mods():
    """ Print modules in order """
    global mod_lib
    log.info('Module Order: '+str([mod.name for mod in mod_lib])[1:-1]+'\n')

def change_mod_status(name, action):
    global mod_lib
    response = {
        'en' : {
            'already_done' : "{mod_name} is already {action}d",
            'successful' : "{mod_name} {action}d",
            'unsuccessful' : "Unable to {action} {mod_name}"
        }
    }
    
    action_already_done = False
    success = False
    for mod in mod_lib:
        mod_name = mod.name.lower().strip().replace('_', '')
        if name in mod_name:
            old_mod_state = mod.enabled
            if action == 'enable':
                mod.enabled = True
            elif action == 'disable':
                mod.enabled = False
            
            if old_mod_state == mod.enabled:
                resp = response[settings.LANG_CODE]['already_done'].format(mod_name=mod_name,
                                                                           action=action)
                return resp
            success = True
            break

    if success:
        resp = response[settings.LANG_CODE]['successful'].format(mod_name=mod_name,
                                                                 action=action)
    else:
        resp = response[settings.LANG_CODE]['unsuccessful'].format(mod_name=mod_name,
                                                                   action=action)
    return resp

def disable_mod(name):
    """ Attempts to disable the specified mod """
    return change_mod_status(name, 'disable')
    
def enable_mod(name):
    """ Attempts to enable the specified mod """
    return change_mod_status(name, 'enable')

def get_from_dict(dict, enabled=True, is_response=False):
    if enabled:
        if not is_response:
            return dict[settings.LANG_4CODE]
        else:
            return dict[settings.LANG_CODE]
    else:
        return []