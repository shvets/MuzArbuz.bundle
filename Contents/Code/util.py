import sys
import os

from datetime import date

def add_pagination_to_response(response, page):
    page = int(page)

    pages = float(response['meta']['total_count']) / float(get_elements_per_page())

    if pages > int(pages):
        pages = int(pages)+1
    else:
        pages = int(pages)

    response['data'] = {'pagination': {
        'page': page,
        'pages': pages,
        'has_next': page < pages,
        'has_previous': page > 1
    }}

def get_language():
    return Prefs['language'].split('/')[1]

def get_elements_per_page():
    return int(Prefs['elements_per_page'])

# def get_format():
#     if Prefs['format'] == 'MP4':
#         return 'mp4'
#     elif Prefs['format'] == 'WMV':
#         return 'wmv'
#     elif Prefs['format'] == 'All Formats':
#         return None
#     else:
#        return None
#
# def get_quality_level():
#     if Prefs['quality_level'] == 'Best':
#         return 4
#     elif Prefs['quality_level'] == 'High':
#         return 3
#     elif Prefs['quality_level'] == 'Medium':
#         return 2
#     elif Prefs['quality_level'] == 'Low':
#         return 1
#     elif Prefs['quality_level'] == "All Levels":
#         return None
#     else:
#         return None

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