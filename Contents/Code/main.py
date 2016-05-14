# -*- coding: utf-8 -*-

from media_info import MediaInfo
import util
import constants
import pagination
from flow_builder import FlowBuilder

from muz_arbuz_plex_service import MuzArbuzPlexService

service = MuzArbuzPlexService()

builder = FlowBuilder()

CYRILLIC_LETTERS = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С',
                    'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я']

LATIN_LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

@route(constants.PREFIX + '/albums')
def HandleAlbums(title, page=1, **params):
    oc = ObjectContainer(title2=unicode(L(title)))

    page = int(page)
    limit = util.get_elements_per_page()
    offset = (page-1)*limit

    response = service.get_albums(limit=limit, offset=offset,
                                  year__gte=util.get_start_music_year(),
                                  year__lte=util.get_end_music_year(),
                                  **filter_params(params))

    oc.title2 = unicode(L(title)) + ' (' + str(response['meta']['total_count']) + ')'

    for media in BuildAlbumsList(response['objects']):
        oc.add(media)

    oc.add(InputDirectoryObject(
            key=Callback(SearchAlbums, title=unicode(L("Albums Search")), page=page),
            title=unicode(L("Albums Search")),
            thumb=R(constants.SEARCH_ICON)
    ))

    util.add_pagination_to_response(response, page)
    pagination.append_controls(oc, response['data'], callback=HandleAlbums, title=title, page=page, **params)

    return oc

def BuildAlbumsList(response):
    list = []

    for media in response:
        id = media['id']
        title = media['title']
        thumb = media['thumbnail']

        if 'is_seria' in media:
            music_container = media['is_seria']
        else:
            music_container = False

        Log(media)

        if 'album' in media:
            new_params = {
                'type': 'album',
                'path': id,
                'album': id,
                'name': title,
                'thumb': thumb,
                'bitrate': "128"
            }
            key = Callback(HandleTracks, **new_params)
        elif music_container:
            new_params = {
                'path': id,
                'parent__id': id,
                'name': title,
                'thumb': thumb
            }
            key = Callback(HandleDoubleAlbum, **new_params)
        else:
            new_params = {
                'path': id,
                'album': id,
                'name': title,
                'thumb': thumb,
                'bitrate': "128"
            }
            key = Callback(HandleTracks, **new_params)

        list.append(DirectoryObject(key=key, title=unicode(title), thumb=thumb))

    return list

@route(constants.PREFIX + '/double_album')
def HandleDoubleAlbum(operation=None, **params):
    oc = ObjectContainer(title2=unicode(params['name']))

    media_info = MediaInfo(**params)

    if operation == 'add':
        service.queue.add(media_info)
    elif operation == 'remove':
        service.queue.remove(media_info)

    response = service.get_albums(limit=util.get_elements_per_page(),
                                  year__gte=util.get_start_music_year(),
                                  year__lte=util.get_end_music_year(),
                                  **filter_params(params))

    for media in response['objects']:
        id = media['id']
        title = media['title']
        thumb = media['thumbnail']

        new_params = {
            'type': 'double_album',
            'album': id,
            'path': id,
            'name': title,
            'thumb': thumb
        }
        key = Callback(HandleTracks, **new_params)
        oc.add(DirectoryObject(key=key, title=unicode(title), thumb=thumb))

    service.queue.append_controls(oc, HandleDoubleAlbum, media_info)

    return oc

@route(constants.PREFIX + '/cyrillic_letters_menu')
def GetCyrillicLettersMenu(title):
    oc = ObjectContainer(title2=unicode(L(title)))

    for letter in CYRILLIC_LETTERS:
        name = L('Letter') + ' ' + letter

        oc.add(DirectoryObject(key=Callback(HandleLetter, title=name, title__istartswith=letter), title=unicode(letter)))

    return oc

@route(constants.PREFIX + '/latin_letters_menu')
def GetLatinLettersMenu(title):
    oc = ObjectContainer(title2=unicode(L(title)))

    for letter in LATIN_LETTERS:
        name = L('Letter') + ' ' + letter

        oc.add(DirectoryObject(key=Callback(HandleLetter, title=name, title__istartswith=letter), title=unicode(letter)))

    return oc

@route(constants.PREFIX + '/letter')
def HandleLetter(title, page=1, **params):
    oc = ObjectContainer(title2=unicode(title))

    page = int(page)
    limit = util.get_elements_per_page()
    offset = (page-1)*limit

    response = service.get_artist_annotated(limit=limit, offset=offset, **params)

    for artist in BuildArtistsList(response['objects']):
        oc.add(artist)

    util.add_pagination_to_response(response, page)
    pagination.append_controls(oc, response['data'], callback=HandleLetter, title=title, page=page, **params)

    oc.add(InputDirectoryObject(
        key=Callback(SearchArtists, title=unicode(L("Artists Search"))),
        title=unicode(L("Artists Search")),
        thumb=R(constants.SEARCH_ICON)
    ))

    return oc

@route(constants.PREFIX + '/artists')
def HandleArtists(title, page=1, **params):
    oc = ObjectContainer(title2=unicode(L(title)))

    page = int(page)
    limit = util.get_elements_per_page()
    offset = (page-1)*limit

    response = service.get_artists(limit=limit, offset=offset, **params)

    oc.title2 = unicode(L(title)) + ' (' + str(response['meta']['total_count']) + ')'

    for artist in BuildArtistsList(response['objects']):
        oc.add(artist)

    util.add_pagination_to_response(response, page)
    pagination.append_controls(oc, response['data'], callback=HandleArtists, title=title, page=page)

    oc.add(InputDirectoryObject(
        key=Callback(SearchArtists, title=unicode(L("Artists Search"))),
        title=unicode(L("Artists Search")),
        thumb=R(constants.SEARCH_ICON)
    ))

    return oc

def BuildArtistsList(response):
    list = []

    for media in response:
        id = media['id']
        title = media['title']
        thumb = media['thumbnail']

        params = {
            'type': 'artist',
            'path': id,
            'id': id,
            'title': L(title),
            'thumb': thumb
        }
        list.append(DirectoryObject(
            key=Callback(HandleArtist, **params),
            title=unicode(L(title)),
            thumb=thumb
        ))

    return list

@route(constants.PREFIX + '/artist')
def HandleArtist(operation=None, **params):
    Log(params)

    oc = ObjectContainer(title2=unicode(L("Artist") + " " + params['title']))

    media_info = MediaInfo(**params)

    if operation == 'add':
        service.queue.add(media_info)
    elif operation == 'remove':
        service.queue.remove(media_info)

    response1 = service.get_albums(artists=params['id'], limit=1, offset=0,
                                   year__gte=util.get_start_music_year(),
                                   year__lte=util.get_end_music_year())
    count1 = int(response1['meta']['total_count'])

    if count1 > 0:
        new_params = {
            'title': unicode(L('Albums')) + " " + params['title'],
            'artists': params['id']
        }
        oc.add(DirectoryObject(
            key=Callback(HandleAlbums, **new_params),
            title=unicode(L('Albums') + ' (' + str(count1) + ')'),
            thumb=media_info['thumb']
        ))

    response2 = service.get_tracks(artists=params['id'], limit=1, offset=0,
                                   year__gte=util.get_start_music_year(),
                                   year__lte=util.get_end_music_year())
    count2 = int(response2['meta']['total_count'])

    if count2 > 0:
        new_params = {
            'type': 'artist',
            'artist': params['id'],
            'path': params['id'],
            'name': L('Audio Tracks') + " " + params['title'],
            'thumb': params['thumb']
        }
        oc.add(DirectoryObject(
            key=Callback(HandleTracks, **new_params),
            title=unicode(L('Audio Tracks') + ' (' + response2['meta']['total_count'] + ')'),
            thumb=params['thumb']
        ))

    service.queue.append_controls(oc, HandleArtist, media_info)

    return oc

@route(constants.PREFIX + '/collections')
def HandleCollections(title, page=1, **params):
    oc = ObjectContainer()

    page = int(page)
    limit = util.get_elements_per_page()
    offset = (page-1)*limit

    response = service.get_collections(limit=limit, offset=offset)

    oc.title2 = unicode(L('Collections')) + ' (' + str(response['meta']['total_count']) + ')'

    for media in response['objects']:
        id = media['id']
        name = media['title']
        thumb = media['thumbnail']

        key = Callback(HandleCollection, collection__id=id, title=name, thumb=thumb)
        oc.add(DirectoryObject(key=key, title=unicode(name), thumb=thumb))

    oc.add(InputDirectoryObject(
        key=Callback(SearchCollections, title=unicode(L("Collections Search"))),
        title=unicode(L("Collections Search")),
        thumb=R(constants.SEARCH_ICON)
    ))

    util.add_pagination_to_response(response, page)
    pagination.append_controls(oc, response['data'], callback=HandleCollections, title=title, page=page)

    return oc

@route(constants.PREFIX + '/collection')
def HandleCollection(operation=None, **params):
    media_info = MediaInfo(**params)

    Log(params)

    if operation == 'add':
        service.queue.add(media_info)
    elif operation == 'remove':
        service.queue.remove(media_info)

    oc = ObjectContainer(title2=unicode(L(params['title'])))

    new_params = {
        'type': 'collection',
        'collection__id': params['collection__id'],
        'path': params['collection__id'],
        'name': params['title'],
        'thumb': params['thumb']
    }
    key = Callback(HandleTracks, **new_params)
    oc.add(DirectoryObject(key=key, title=unicode(params['title']), thumb=params['thumb']))

    service.queue.append_controls(oc, HandleCollection, media_info)

    return oc

@route(constants.PREFIX + '/genres')
def HandleGenres(title):
    oc = ObjectContainer()

    response = service.get_genres(limit=0)
    count = response['meta']['total_count']

    oc.title2 = unicode(L(title)) + ' (' + str(count) + ')'

    for media in response['objects']:
        id = media['id']
        title = media['title']
        thumb = 'thumb'

        key = Callback(HandleMusicGenre, title=title, thumb=thumb, genre__in=id)
        oc.add(DirectoryObject(key=key, title=unicode(title), thumb=thumb))

        oc.add(InputDirectoryObject(key=Callback(HandleSearch), title=unicode(L("Search Music")),
                                    thumb=R(constants.SEARCH_ICON)))

    return oc

@route(constants.PREFIX + '/music_genre')
def HandleMusicGenre(operation=None, **params):
    media_info = MediaInfo(**params)

    if operation == 'add':
        service.queue.add(media_info)
    elif operation == 'remove':
        service.queue.remove(media_info)

    oc = ObjectContainer(title2=unicode(L(params['title'])))

    key = Callback(HandleAlbums, title=params['title'], genre__in=params['genre__in'])
    oc.add(DirectoryObject(key=key, title=unicode(params['title'])))

    service.queue.append_controls(oc, HandleMusicGenre, media_info)

    oc.add(InputDirectoryObject(key=Callback(HandleSearch), title=unicode(L("Search Music")),
                                thumb=R(constants.SEARCH_ICON)))

    return oc

@route(constants.PREFIX + '/tracks')
def HandleTracks(operation=None, page=1, **params):
    media_info = MediaInfo(**params)

    Log(params)

    if 'album' in params:
        media_info['path'] = params['album']

    if operation == 'add':
        service.queue.add(media_info)
    elif operation == 'remove':
        service.queue.remove(media_info)

    oc = ObjectContainer(title2=unicode(params['name']))

    page = int(page)
    limit = util.get_elements_per_page()
    offset = (page-1)*limit

    response = service.get_tracks(limit=util.get_elements_per_page(), offset=offset, **filter_params(params))

    for media in response['objects']:
        title = media['title']
        file = media['file']

        if media['album']['artist']:
            artist = media['album']['artist']['title']
        else:
            artist = ''

        format = 'mp3'
        url = service.BASE_URL + file
        bitrate = "128"

        new_params = {
            'type': 'track',
            'path': url,
            'name': title,
            'thumb': params['thumb'],
            'artist': artist,
            'format': format,
            'bitrate': bitrate
        }

        oc.add(HandleTrack(**new_params))

    service.queue.append_controls(oc, HandleTracks, media_info)

    util.add_pagination_to_response(response, page)
    pagination.append_controls(oc, response['data'], callback=HandleTracks, page=page, **params)

    return oc


VALID_PARAMETERS = ['album', 'artists', 'collection__id']

def filter_params(params):
    return dict((key, value) for key, value in params.iteritems() if key in VALID_PARAMETERS)

@route(constants.PREFIX + '/search')
def HandleSearch(query=None, page=1):
    page = int(page)

    oc = ObjectContainer(title2=unicode(L('Music Search')))

    response = search(q=query, limit=1, offset=0)

    count1 = response['collection']['meta']['total_count']

    if count1:
        oc.add(DirectoryObject(
            key=Callback(SearchCollections, title=L('Collections'), query=query, page=page),
            title=unicode(L('Collections') + " (" + str(count1) + ")")
        ))

    count2 = response['artist_annotated']['meta']['total_count']

    if count2:
        oc.add(DirectoryObject(
            key=Callback(SearchArtists, type='artist_annotated', title=L('Artists'), query=query, page=page),
            title=unicode(L('Artists') + " (" + str(count2) + ")")
        ))

    count3 = response['album']['meta']['total_count']

    if count3:
        oc.add(DirectoryObject(
            key=Callback(SearchAlbums, title=L('Albums'), query=query, page=page),
            title=unicode(L('Albums') + " (" + str(count3) + ")")
        ))

    count4 = response['audio_track']['meta']['total_count']

    if count4:
        oc.add(DirectoryObject(
            key=Callback(SearchTracks, title=L('Audio Tracks'), query=query, page=page),
            title=unicode(L('Audio Tracks') + " (" + str(count4) + ")")
        ))

    return oc

@route(constants.PREFIX + '/search_tracks')
def SearchTracks(title, query, page, **params):
    oc = ObjectContainer(title2=unicode(L(title)))

    page = int(page)
    limit = util.get_elements_per_page()
    offset = (page-1)*limit

    response = service.search_audio_track(q=query, limit=util.get_elements_per_page(), offset=offset)

    for media in response['objects']:
        title = media['title']
        thumb = 'thumb'
        file = media['file']
        if media['album']['artist']:
            artist = media['album']['artist']['title']
        else:
            artist = ''

        format = 'mp3'
        url = service.BASE_URL + file

        oc.add(HandleTrack(path=url, name=unicode(title), thumb=thumb, artist=artist, format=format))

    util.add_pagination_to_response(response, page)
    pagination.append_controls(oc, response['data'], callback=SearchTracks, title=title, query=query, page=page, **params)

    return oc

@route(constants.PREFIX + '/search_artists')
def SearchArtists(title, query, page, **params):
    oc = ObjectContainer(title2=unicode(L(title)))

    page = int(page)
    limit = util.get_elements_per_page()
    offset = (page-1)*limit

    response = service.search_artist_annotated(q=query, limit=util.get_elements_per_page(), offset=offset)

    for artist in BuildArtistsList(response['objects']):
        oc.add(artist)

    util.add_pagination_to_response(response, page)
    pagination.append_controls(oc, response['data'], callback=SearchArtists, title=title, query=query, page=page, **params)

    return oc

@route(constants.PREFIX + '/search_albums')
def SearchAlbums(title, query, page=1, **params):
    oc = ObjectContainer(title2=unicode(L(title)))

    page = int(page)
    limit = util.get_elements_per_page()
    offset = (page-1)*limit

    response = service.search_album(q=query, limit=util.get_elements_per_page(), offset=offset)

    for media in BuildAlbumsList(response['objects']):
        oc.add(media)

    util.add_pagination_to_response(response, page)
    pagination.append_controls(oc, response['data'], callback=SearchAlbums, title=title, query=query, page=page, **params)

    return oc

@route(constants.PREFIX + '/search_collections')
def SearchCollections(title, query, page=1, **params):
    page = int(page)
    limit = util.get_elements_per_page()
    offset = (page-1)*limit

    oc = ObjectContainer(title2=unicode(L(title)))

    response = service.search_collection(q=query, limit=util.get_elements_per_page(), offset=offset)

    for media in BuildArtistsList(response['objects']):
        oc.add(media)

    util.add_pagination_to_response(response, page)
    pagination.append_controls(oc, response['data'], callback=SearchCollections, title=title, query=query, page=page, **params)

    return oc

@route(constants.PREFIX + '/track')
def HandleTrack(container=False, **params):
    media_info = MediaInfo(**params)

    if 'm4a' in media_info['format']:
        audio_container = Container.MP4
        audio_codec = AudioCodec.AAC
    else:
        audio_container = Container.MP3
        audio_codec = AudioCodec.MP3

    if 'duration' in media_info:
        duration = media_info['duration']
    else:
        duration = 0

    url_items = [
        {
            "url": media_info['path'],
            "config": {
                "container": audio_container,
                "audio_codec": audio_codec,
                "bitrate": media_info['bitrate'],
                "duration": duration
            }
        }
    ]

    track = AudioMetadataObjectForURL(media_info, url_items=url_items, player=PlayAudio)

    if container:
        oc = ObjectContainer(title2=unicode(media_info['name']))

        oc.add(track)

        return oc
    else:
        return track

def AudioMetadataObjectForURL(media_info, url_items, player):
    metadata_object = builder.build_metadata_object(media_type=media_info['type'], title=media_info['name'])

    metadata_object.key = Callback(HandleTrack, container=True, **media_info)
    metadata_object.rating_key = unicode(media_info['name'])
    metadata_object.thumb = media_info['thumb']

    if 'duration' in media_info:
        metadata_object.duration = int(media_info['duration']) * 1000

    if 'artist' in media_info:
        metadata_object.artist = media_info['artist']

    metadata_object.items.extend(MediaObjectsForURL(url_items, player))

    return metadata_object

@route(constants.PREFIX + '/container')
def HandleContainer(**params):
    type = params['type']

    if type == 'artist':
        return HandleArtist(**params)
    elif type == 'album':
        return HandleTracks(**params)
    elif type == 'collection__id':
        return HandleTracks(**params)
    elif type == 'genre__in':
        return HandleAlbums(**params)
    elif type == 'parent__id':
        return HandleDoubleAlbum(**params)

# @route(constants.PREFIX + '/queue')
# def GetQueue(title, filter=None):
#     oc = ObjectContainer(title2=unicode(L(title)))
#
#     for media in service.queue.data:
#         type = media['type']
#
#         if type == filter:
#             id = media['id']
#             name = media['name']
#
#             if 'thumb' in media:
#                 thumb = media['thumb']
#             else:
#                 thumb = 'thumb'
#
#             if filter == 'audio_tracks':
#                 key = Callback(audio_tracks.HandleAudioTracks, album=id, name=name, thumb=thumb)
#                 oc.add(DirectoryObject(key=key, title=unicode(name), thumb=thumb))
#             elif filter == 'album':
#                 key = Callback(audio_tracks.HandleAudioTracks, album=id, name=name, thumb=thumb)
#                 oc.add(DirectoryObject(key=key, title=unicode(name), thumb=thumb))
#             elif filter == 'artists':
#                 key=Callback(artists.GetArtistMenu, id=id, title=L(name), thumb=thumb)
#                 oc.add(DirectoryObject(key=key, title=unicode(L(name)), thumb=thumb
#             ))
#             elif filter == 'collection__id':
#                 key = Callback(audio_tracks.HandleAudioTracks, collection__id=id, name=name, thumb=thumb)
#                 oc.add(DirectoryObject(key=key, title=unicode(name), thumb=thumb))
#             elif filter == 'genre__in':
#                 key = Callback(HandleAlbums, title=name, genre__in=id)
#                 oc.add(DirectoryObject(key=key, title=unicode(name)))
#             elif filter == 'parent__id':
#                 key = Callback(HandleDoubleAlbum, name=name, parent__id=id, thumb=thumb)
#                 oc.add(DirectoryObject(key=key, title=unicode(name), thumb=thumb))
#
# oc.add(InputDirectoryObject(key=Callback(HandleSearch), title=unicode(L("Search Music")),
#                             thumb=R(constants.SEARCH_ICON)))
#
#     return oc
#
# def get_type(params):
#     if 'album' in params:
#         type = 'album'
#     elif 'collection__id' in params:
#         type = 'collection__id'
#     elif 'artists' in params:
#         type = 'artists'
#     elif 'audio_tracks' in params:
#         type = 'audio_tracks'
#     elif 'genre__in' in params:
#         type = 'genre__in'
#     elif 'parent__id' in params:
#         type = 'parent__id'
#     else:
#         type = None
#
#     return type
#
# def item_already_added_to_storage(type, id):
#     added = False
#
#     for media in service.queue.data:
#         if id == media['id']:
#             added = True
#             break
#
#     return added

@route(constants.PREFIX + '/queue')
def HandleQueue():
    oc = ObjectContainer(title2=unicode(L('Queue')))

    for media_info in service.queue.data:
        if 'thumb' in media_info:
            thumb = media_info['thumb']
        else:
            thumb = None

        oc.add(DirectoryObject(
            key=Callback(HandleContainer, **media_info),
            title=util.sanitize(media_info['name']),
            thumb=thumb
        ))

    if len(service.queue.data) > 0:
        oc.add(DirectoryObject(
            key=Callback(ClearQueue),
            title=unicode(L("Clear Queue"))
        ))

    return oc

@route(constants.PREFIX + '/clear_queue')
def ClearQueue():
    service.queue.clear()

    return HandleQueue()

@route(constants.PREFIX + '/history')
def HandleHistory():
    history_object = history.load_history()

    oc = ObjectContainer(title2=unicode(L('History')))

    if history_object:
        for item in sorted(history_object.values(), key=lambda k: k['time'], reverse=True):
            oc.add(DirectoryObject(
                key=Callback(HandleContainer, **item),
                title=unicode(item['name']),
                thumb=item['thumb']
            ))

    return oc

def MediaObjectsForURL(url_items, player):
    media_objects = []

    for item in url_items:
        url = item['url']
        config = item['config']

        play_callback = Callback(player, url=url)

        media_object = builder.build_media_object(play_callback, config)

        media_objects.append(media_object)

    return media_objects

@route(constants.PREFIX + '/play_audio')
def PlayAudio(url):
    return Redirect(url)