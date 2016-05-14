import sys
import os

from datetime import date

def get_language():
    return Prefs['language'].split('/')[1]

def get_elements_per_page():
    return int(Prefs['elements_per_page'])

def get_start_music_year():
    value = Prefs['start_music_year']

    if value == 'Now':
        return date.today().year
    else:
        return value

def get_end_music_year():
    value = Prefs['end_music_year']

    if value == 'Now':
        return date.today().year
    else:
        return value

def validate_prefs():
    language = get_language()

    if Core.storage.file_exists(Core.storage.abs_path(
        Core.storage.join_path(Core.bundle_path, 'Contents', 'Strings', '%s.json' % language)
    )):
        Locale.DefaultLocale = language
    else:
        Locale.DefaultLocale = 'en-us'

def no_contents(name=None):
    if not name:
        name = 'Error'

    return ObjectContainer(header=unicode(L(name)), message=unicode(L('No entries found')))

def sanitize(name):
    return unicode(name[0:35])

def add_library(path):
    lib_path = Core.storage.abs_path(Core.storage.join_path(Core.bundle_path, 'Contents', 'Code', path))

    Log(Core.storage.join_path(Core.bundle_path, 'Contents', 'Code', path))

    sys.path.append(os.path.abspath(os.path.join(lib_path)))