"""
A simple test script to see input phrases are being picked up by the expected task.
The test uses a text file as input from tests/regex_phrases/ folder for phrases to
test, where the file name is {LANG_4CODE}.txt and which file is selected depends
on settings.LANG_4CODE. 

Only regex is matched and task matched printed out, without execution of the task.

Only tasks in enabled modules will be matched.
"""
print('---- Running Regex Test ----')

import sys
import os.path

import traceback
import time
import argparse

from athena import settings, mods
from athena.brain import Brain


def parse_phrases_file_to_dict(only_modules):
    phrase_folder = "regex_phrases"
    dir = os.path.dirname(__file__)
    file_path = "{dir}\\{phrase_folder}\\{speech_language}.txt".format(dir=dir,
                                                                       phrase_folder=phrase_folder,
                                                                       speech_language=settings.LANG_4CODE)
    if not os.path.isfile(file_path):
        error = "No phrase file exists in folder {phrase_folder} for the ".format(phrase_folder=phrase_folder)
        error += "selected speech language ({speech_language}). The file name ".format(speech_language=settings.LANG_4CODE)
        error += "should be '{speech_language}.txt'".format(speech_language=settings.LANG_4CODE)
        sys.exit(error)
    
    phrases = {}
    lines = [line.rstrip('\n') for line in open(file_path)]
    for line in lines:
        if line[:1] == "#":
            continue
        elif line[:2] == "::":
            module_name = line[2:]
            phrases[module_name] = {}
        elif line[:1] == ":":
            task_name = line[1:]
            phrases[module_name][task_name] = []
        elif line:
            if (not only_modules 
                    or module_name in only_modules):
                phrases[module_name][task_name].append(line)

    return phrases

    
def handle_results(tasks, type):
    message_multiple = ""
    if type == "multiple":
        for task in tasks:
            message_multiple += "'{test_module_name}.{test_task_name}'\n".format(test_module_name=task['module_name'],
                                                                                 test_task_name=task['task_name'])
        message = "Expected task '{test_module_name}.{test_task_name}', got multiple:\n{multiple}"
    else:
        if type == "single":
            message = "Found the correct task : {test_module_name}.{test_task_name}"
        elif type == "wrong":
            message = "Expected task '{test_module_name}.{test_task_name}', got '{module_name}.{task_name}'"
        elif type == "none":
                message = "Expected task '{test_module_name}.{test_task_name}' but no task was found"

    message = message.format(test_task_name=tasks[0]['test_task_name'],
                             test_module_name=tasks[0]['test_module_name'],
                             task_name=tasks[0]['task_name'],
                             module_name=tasks[0]['module_name'],
                             multiple=message_multiple)

    print("-------------------------------------")
    print("Testing phrase: '{}'".format(tasks[0]['phrase']))
    print("-------------------------------------")
    print(message)
    print()

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-s', '--speech-language',
                        dest='speech_language',
                        default=settings.LANG_4CODE,
                        help="Specify a language on LCID format (see settings.py for help). Defaults to settings.LANG_4CODE.")
    parser.add_argument('-r', '--response-language',
                        dest='response_language',
                        default=settings.LANG_CODE,
                        help="Specify a language in two characer format (see settings.py for help). Defaults to settings.LANG_CODE.")
    parser.add_argument('-p', '--print-passed',
                        dest='print_passed',
                        action='store_true',
                        help="Determines if passed tests are printed out.")
    parser.add_argument('-e', '--execute',
                        dest='execute',
                        action='store_true',
                        default=False,
                        help="Determines if matched tasks are executed.")
    parser.add_argument('-m', '--modules',
                        dest='only_modules',
                        nargs='*',
                        help="Overwrite which modules should be tested. Unrecognized modules will be ignored.")

    args = parser.parse_args()
    
    settings.LANG_4CODE = args.speech_language
    settings.LANG_CODE = args.response_language
    
    settings.USE_STT = False
    settings.USE_TTS = False
    my_brain = Brain(greet_user=False)
    
    test_modules = parse_phrases_file_to_dict(args.only_modules)
    for test_module_name, test_tasks in test_modules.items():
        for test_task_name, phrases in test_tasks.items():
            for phrase in phrases:
                tasks = []
                my_brain.match_mods(phrase)
                modules = my_brain.execute_mods(phrase, no_execution=not args.execute)
                for module in modules:
                    for task in module.task_queue:
                        task_name = type(task).__name__
                        task_dict = {
                            'task_name'        : task_name,
                            'module_name'      : module.name,
                            'match'            : task_name == test_task_name,
                            'found'            : task_name != 'AnswerTask',
                            'test_task_name'   : test_task_name,
                            'test_module_name' : test_module_name,
                            'phrase'           : phrase
                        }
                        tasks.append(task_dict)
                if not tasks:
                    task_dict = {
                        'task_name'        : "",
                        'module_name'      : "",
                        'match'            : False,
                        'not_found'        : True,
                        'test_task_name'   : test_task_name,
                        'test_module_name' : test_module_name,
                        'phrase'           : phrase
                    }
                    tasks.append(task_dict)

                if len(tasks) > 1:
                    handle_results(tasks, "multiple")
                elif not tasks[0]['found']:
                    handle_results(tasks, "none")
                elif not tasks[0]['match']:
                    handle_results(tasks, "wrong")
                elif args.print_passed:
                    handle_results(tasks, "single")
    print('---- Regex Test Finished ----')
    
if __name__ == '__main__':
    main()
    