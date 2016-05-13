# -*- coding: utf-8 -*-

import constants

@route(constants.PREFIX + '/albums_menu')
def GetAlbumsMenu(title):
    oc = ObjectContainer(title2=unicode(L(title)))

    oc.add(DirectoryObject(
            key=Callback(HandleAlbums, title=L('All Albums')),
            title=unicode(L('All Albums'))
    ))
    oc.add(DirectoryObject(
            key=Callback(music_queue.GetQueue, filter='album', title=L('Favorite Albums')),
            title=unicode(L('Favorite Albums'))))
    oc.add(DirectoryObject(
            key=Callback(music_queue.GetQueue, filter='parent__id', title=L('Favorite Double Albums')),
            title=unicode(L('Favorite Double Albums'))))

    oc.add(InputDirectoryObject(
            key=Callback(SearchMusicAlbums, title=unicode(L("Albums Search"))),
            title=unicode(L("Albums Search")),
            thumb=R(constants.SEARCH_ICON)
    ))

    return oc

@route(constants.PREFIX + '/search_music_albums')
def SearchMusicAlbums(title, query, page=1, **params):
    oc = ObjectContainer(title2=unicode(L(title)))

    page = int(page)
    limit = util.get_elements_per_page()
    offset = (page-1)*limit

    response = service.search_album(q=query, limit=util.get_elements_per_page(), offset=offset)

    for media in BuildAlbumsList(response['objects']):
        oc.add(media)

    util.add_pagination_to_response(response, page)
    pagination.append_controls(oc, response['data'], callback=SearchMusicAlbums, title=title, query=query, page=page, **params)

    return oc

@route(constants.PREFIX + '/albums')
def HandleAlbums(title, page=1, **params):
    oc = ObjectContainer(title2=unicode(L(title)))

    page = int(page)
    limit = util.get_elements_per_page()
    offset = (page-1)*limit

    response = service.get_albums(limit=limit, offset=offset,
                                  year__gte=util.get_start_music_year(),
                                  year__lte=util.get_end_music_year(),
                                  **params)

    oc.title2 = unicode(L(title)) + ' (' + str(response['meta']['total_count']) + ')'

    for media in BuildAlbumsList(response['objects']):
        oc.add(media)

    oc.add(InputDirectoryObject(
            key=Callback(SearchMusicAlbums, title=unicode(L("Albums Search")), page=page),
            title=unicode(L("Albums Search")),
            thumb=R(constants.SEARCH_ICON)
    ))

    util.add_pagination_to_response(response, page)
    pagination.append_controls(oc, response['data'], callback=HandleAlbums, title=title, page=page, **params)

    return oc

def BuildAlbumsList(response, **params):
    list = []

    for media in response:
        id = media['id']
        title = media['title']
        thumb = media['thumbnail']

        if 'is_seria' in media:
            music_container = media['is_seria']
        else:
            music_container = False

        if 'album' in media:
            key = Callback(HandleAudioTracks, album=id, name=title, thumb=thumb, **params)
        elif music_container:
            key = Callback(HandleDoubleAlbum, parent__id=id, name=title, thumb=thumb, **params)
        else:
            key = Callback(HandleAudioTracks, album=id, name=title, thumb=thumb, **params)

        list.append(DirectoryObject(key=key, title=unicode(title), thumb=thumb))

    return list

@route(constants.PREFIX + '/double_album')
def HandleDoubleAlbum(name, thumb, **params):
    oc = ObjectContainer(title2=unicode(name))

    response = service.get_albums(limit=util.get_elements_per_page(),
                                  year__gte=util.get_start_music_year(),
                                  year__lte=util.get_end_music_year(),
                                  **params)

    for media in response['objects']:
        id = media['id']
        title = media['title']
        thumb = media['thumbnail']

        key = Callback(HandleAudioTracks, album=id, name=title, thumb=thumb)
        oc.add(DirectoryObject(key=key, title=unicode(title), thumb=thumb))

    music_queue.append_controls(oc, name=name, thumb=thumb, **params)

    return oc

CYRILLIC_LETTERS = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С',
                    'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я']

LATIN_LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

@route(constants.PREFIX + '/artists_menu')
def GetArtistsMenu(title):
    oc = ObjectContainer(title2=unicode(L(title)))

    oc.add(DirectoryObject(
            key=Callback(HandleArtists, title=L('All Artists')),
            title=unicode(L('All Artists'))
    ))
    oc.add(DirectoryObject(
            key=Callback(GetCyrillicLettersMenu, title=L('By Letter')),
            title=unicode(L('By Letter'))
    ))
    oc.add(DirectoryObject(
            key=Callback(GetLatinLettersMenu, title=L('By Latin Letter')),
            title=unicode(L('By Latin Letter'))
    ))
    oc.add(DirectoryObject(
            key=Callback(music_queue.GetQueue, filter='artists', title=L('Favorite Artists')),
            title=unicode(L('Favorite Artists'))
    ))

    add_search_artists(oc)

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

    add_search_artists(oc)

    return oc

@route(constants.PREFIX + '/search_music_artists')
def SearchMusicArtists(title, query, page, **params):
    oc = ObjectContainer(title2=unicode(L(title)))

    page = int(page)
    limit = util.get_elements_per_page()
    offset = (page-1)*limit

    response = service.search_artist_annotated(q=query, limit=util.get_elements_per_page(), offset=offset)

    for artist in BuildArtistsList(response['objects']):
        oc.add(artist)

    util.add_pagination_to_response(response, page)
    pagination.append_controls(oc, response['data'], callback=SearchMusicArtists, title=title, query=query, page=page, **params)

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

    add_search_artists(oc)

    return oc

def BuildArtistsList(response):
    list = []

    for media in response:
        id = media['id']
        title = media['title']
        thumb = media['thumbnail']

        list.append(DirectoryObject(
                key=Callback(GetArtistMenu, id=id, title=L(title), thumb=thumb),
                title=unicode(L(title)),
                thumb=thumb
        ))

    return list

@route(constants.PREFIX + '/artist_menu')
def GetArtistMenu(id, title, thumb, **params):
    oc = ObjectContainer(title2=unicode(L("Artist") + " " + title))

    response1 = service.get_albums(artists=id, limit=1, offset=0,
                                   year__gte=util.get_start_music_year(),
                                   year__lte=util.get_end_music_year())
    count1 = int(response1['meta']['total_count'])

    if count1 > 0:
        oc.add(DirectoryObject(
            key=Callback(albums.HandleAlbums, title=unicode(L('Albums')) + " " + title, artists=id),
            title=unicode(L('Albums') + ' (' + str(count1) + ')'),
            thumb=thumb
        ))

    response2 = service.get_tracks(artists=id, limit=1, offset=0,
                                   year__gte=util.get_start_music_year(),
                                   year__lte=util.get_end_music_year())
    count2 = int(response2['meta']['total_count'])

    if count2 > 0:
        oc.add(DirectoryObject(
            key=Callback(HandleAudioTracks, name=L('Audio Tracks') + " " + title, thumb=thumb, artists=id),
            title=unicode(L('Audio Tracks') + ' (' + response2['meta']['total_count'] + ')'),
            thumb=thumb
        ))

    music_queue.append_controls(oc, name=title, artists=id, thumb=thumb)

    return oc

def add_search_artists(oc):
    oc.add(InputDirectoryObject(
        key=Callback(SearchMusicArtists, title=unicode(L("Artists Search"))),
        title=unicode(L("Artists Search")),
        thumb=R(constants.SEARCH_ICON)
    ))

@route(constants.PREFIX + '/collections_menu')
def GetCollectionsMenu(title):
    oc = ObjectContainer(title2=unicode(L(title)))

    oc.add(DirectoryObject(
            key=Callback(HandleCollections, title=L('All Collections')),
            title=unicode(L('All Collections'))
    ))
    oc.add(DirectoryObject(
            key=Callback(music_queue.GetQueue, filter='collection__id', title=L('Favorite Collections')),
            title=unicode(L('Favorite Collections'))
    ))

    add_search_collections(oc)

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

    add_search_collections(oc)

    util.add_pagination_to_response(response, page)
    pagination.append_controls(oc, response['data'], callback=HandleCollections, title=title, page=page)

    return oc

@route(constants.PREFIX + '/collection')
def HandleCollection(title, collection__id, thumb):
    oc = ObjectContainer(title2=unicode(L(title)))

    key = Callback(HandleAudioTracks, name=title, collection__id=collection__id, thumb=thumb)
    oc.add(DirectoryObject(key=key, title=unicode(title), thumb=thumb))

    music_queue.append_controls(oc, name=title, thumb=thumb, collection__id=collection__id)

    return oc

@route(constants.PREFIX + '/search_music_collections')
def SearchMusicCollections(title, query, page=1, **params):
    page = int(page)
    limit = util.get_elements_per_page()
    offset = (page-1)*limit

    oc = ObjectContainer(title2=unicode(L(title)))

    response = service.search_collection(q=query, limit=util.get_elements_per_page(), offset=offset)

    for media in artists.BuildArtistsList(response['objects']):
        oc.add(media)

    util.add_pagination_to_response(response, page)
    pagination.append_controls(oc, response['data'], callback=SearchMusicCollections, title=title, query=query, page=page, **params)

    return oc

def add_search_collections(oc):
    oc.add(InputDirectoryObject(
        key=Callback(SearchMusicCollections, title=unicode(L("Collections Search"))),
        title=unicode(L("Collections Search")),
        thumb=R(constants.SEARCH_ICON)
    ))

@route(constants.PREFIX + '/genres_menu')
def GetGenresMenu(title):
    oc = ObjectContainer(title2=unicode(L(title)))

    oc.add(DirectoryObject(
            key=Callback(HandleMusicGenres, title=L('All Genres')),
            title=unicode(L('All Genres'))
    ))

    oc.add(DirectoryObject(
            key=Callback(music_queue.GetQueue, filter='genre__in', title=L('Favorite Genres')),
            title=unicode(L('Favorite Genres'))
    ))

    search.add_search_music(oc)

    return oc

@route(constants.PREFIX + '/music_genres')
def HandleMusicGenres(title):
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

        search.add_search_music(oc)

    return oc

@route(constants.PREFIX + '/music_genre')
def HandleMusicGenre(title, genre__in, thumb):
    oc = ObjectContainer(title2=unicode(L(title)))

    key = Callback(albums.HandleAlbums, title=title, genre__in=genre__in)
    oc.add(DirectoryObject(key=key, title=unicode(title)))

    music_queue.append_controls(oc, name=title, thumb=thumb, genre__in=genre__in)

    search.add_search_music(oc)

    return oc

@route(constants.PREFIX + '/search_music')
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
            key=Callback(SearchMusicAudioTracks, title=L('Audio Tracks'), query=query, page=page),
            title=unicode(L('Audio Tracks') + " (" + str(count4) + ")")
        ))

    return oc

def add_search_music(oc):
    oc.add(InputDirectoryObject(key=Callback(SearchMusic), title=unicode(L("Search Music")), thumb=R(constants.SEARCH_ICON)))

import util
import constants
import music_queue
import pagination
from flow_builder import FlowBuilder

builder = FlowBuilder()

@route(constants.PREFIX + '/search_music_audio_tracks')
def SearchMusicAudioTracks(title, query, page, **params):
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

        oc.add(GetAudioTrack(path=url, name=unicode(title), thumb=thumb, artist=artist, format=format))

    util.add_pagination_to_response(response, page)
    pagination.append_controls(oc, response['data'], callback=SearchMusicAudioTracks, title=title, query=query, page=page, **params)

    return oc

@route(constants.PREFIX + '/audio_tracks')
def HandleAudioTracks(name, thumb, page=1, **params):
    oc = ObjectContainer(title2=unicode(name))

    page = int(page)
    limit = util.get_elements_per_page()
    offset = (page-1)*limit

    response = service.get_tracks(limit=util.get_elements_per_page(), offset=offset, **params)

    for media in response['objects']:
        title = media['title']
        file = media['file']

        if media['album']['artist']:
            artist = media['album']['artist']['title']
        else:
            artist = ''

        format = 'mp3'
        url = service.BASE_URL + file

        oc.add(GetAudioTrack(path=url, name=unicode(title), thumb=thumb, artist=artist, format=format))

    music_queue.append_controls(oc, name=name, thumb=thumb, **params)

    util.add_pagination_to_response(response, page)
    pagination.append_controls(oc, response['data'], callback=HandleAudioTracks, name=name, thumb=thumb, page=page, **params)

    return oc

@route(constants.PREFIX + '/audio_track')
def GetAudioTrack(path, name, thumb, artist, format, container=False):
    if 'm4a' in format:
        audio_container = Container.MP4
        audio_codec = AudioCodec.AAC
    else:
        audio_container = Container.MP3
        audio_codec = AudioCodec.MP3

    url_items = [
        {
            "url": path,
            "config": {
                "container": audio_container,
                "audio_codec": audio_codec,
                "bitrate": "128"
            }
        }
    ]

    track = MetadataObjectForURL("track", path=path, name=name, thumb=thumb, artist=artist, format=format,
                                 url_items=url_items, player=PlayAudio)
    if container:
        oc = ObjectContainer(title2=unicode(name))

        oc.add(track)

        return oc
    else:
        return track

def MetadataObjectForURL(media_type, path, name, thumb, artist, format, url_items, player):
    metadata_object = builder.build_metadata_object(media_type=media_type, title=name)

    metadata_object.key = Callback(GetAudioTrack, path=path, name=name, thumb=thumb, artist=artist,
                                   format=format, container=True)
    metadata_object.rating_key = unicode(name)
    #metadata_object.title = unicode(title)
    #metadata_object.album = 'album'
    #metadata_object.thumb = thumb
    metadata_object.artist = artist

    metadata_object.items = MediaObjectsForURL(url_items, player)

    return metadata_object

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