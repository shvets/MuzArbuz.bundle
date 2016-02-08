from datetime import date

import albums
import artists
import collections
import audio_tracks

@route('/music/music/search_music')
def SearchMusic(query=None, page=1, **params):
    page = int(page)

    oc = ObjectContainer(title2=unicode(L('Music Search')))

    response = service.search(q=query, limit=1, offset=0)

    count1 = response['collection']['meta']['total_count']

    if count1:
        oc.add(DirectoryObject(
            key=Callback(collections.SearchMusicCollections, title=L('Collections'), query=query, page=page),
            title=unicode(L('Collections') + " (" + str(count1) + ")")
        ))

    count2 = response['artist_annotated']['meta']['total_count']

    if count2:
        oc.add(DirectoryObject(
            key=Callback(artists.SearchMusicArtists, type='artist_annotated', title=L('Artists'), query=query, page=page),
            title=unicode(L('Artists') + " (" + str(count2) + ")")
        ))

    count3 = response['album']['meta']['total_count']

    if count3:
        oc.add(DirectoryObject(
            key=Callback(albums.SearchMusicAlbums, title=L('Albums'), query=query, page=page),
            title=unicode(L('Albums') + " (" + str(count3) + ")")
        ))

    count4 = response['audio_track']['meta']['total_count']

    if count4:
        oc.add(DirectoryObject(
            key=Callback(audio_tracks.SearchMusicAudioTracks, title=L('Audio Tracks'), query=query, page=page),
            title=unicode(L('Audio Tracks') + " (" + str(count4) + ")")
        ))

    return oc

def add_search_music(oc):
    oc.add(InputDirectoryObject(key=Callback(SearchMusic), title=unicode(L("Search Music")), thumb=R(SEARCH_ICON)))

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
