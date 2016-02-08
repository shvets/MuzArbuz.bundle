# -*- coding: utf-8 -*-

import common
import music_queue
import pagination
import albums
import audio_tracks

CYRILLIC_LETTERS = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С',
                    'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я']

LATIN_LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

@route('/music/music/artists_menu')
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

@route('/music/music/cyrillic_letters_menu')
def GetCyrillicLettersMenu(title):
    oc = ObjectContainer(title2=unicode(L(title)))

    for letter in CYRILLIC_LETTERS:
        name = L('Letter') + ' ' + letter

        oc.add(DirectoryObject(key=Callback(HandleLetter, title=name, title__istartswith=letter), title=unicode(letter)))

    return oc

@route('/music/music/latin_letters_menu')
def GetLatinLettersMenu(title):
    oc = ObjectContainer(title2=unicode(L(title)))

    for letter in LATIN_LETTERS:
        name = L('Letter') + ' ' + letter

        oc.add(DirectoryObject(key=Callback(HandleLetter, title=name, title__istartswith=letter), title=unicode(letter)))

    return oc

@route('/music/music/letter')
def HandleLetter(title, page=1, **params):
    oc = ObjectContainer(title2=unicode(title))

    page = int(page)
    limit = common.get_elements_per_page()
    offset = (page-1)*limit

    response = service.get_artist_annotated(limit=limit, offset=offset, **params)

    for artist in BuildArtistsList(response['objects']):
        oc.add(artist)

    common.add_pagination_to_response(response, page)
    pagination.append_controls(oc, response, callback=HandleLetter, title=title, page=page, **params)

    add_search_artists(oc)

    return oc

@route('/music/music/search_music_artists')
def SearchMusicArtists(title, query, page, **params):
    oc = ObjectContainer(title2=unicode(L(title)))

    page = int(page)
    limit = common.get_elements_per_page()
    offset = (page-1)*limit

    response = service.search_artist_annotated(q=query, limit=common.get_elements_per_page(), offset=offset)

    for artist in BuildArtistsList(response['objects']):
        oc.add(artist)

    common.add_pagination_to_response(response, page)
    pagination.append_controls(oc, response, callback=SearchMusicArtists, title=title, query=query, page=page, **params)

    return oc

@route('/music/music/artists')
def HandleArtists(title, page=1, **params):
    oc = ObjectContainer(title2=unicode(L(title)))

    page = int(page)
    limit = common.get_elements_per_page()
    offset = (page-1)*limit

    response = service.get_artists(limit=limit, offset=offset, **params)

    oc.title2 = unicode(L(title)) + ' (' + str(response['meta']['total_count']) + ')'

    for artist in BuildArtistsList(response['objects']):
        oc.add(artist)

    common.add_pagination_to_response(response, page)
    pagination.append_controls(oc, response, callback=HandleArtists, title=title, page=page)

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

@route('/music/music/artist_menu')
def GetArtistMenu(id, title, thumb, **params):
    oc = ObjectContainer(title2=unicode(L("Artist") + " " + title))

    response1 = service.get_albums(artists=id, limit=1, offset=0,
                                         year__gte=common.get_start_music_year(),
                                         year__lte=common.get_end_music_year())
    count1 = int(response1['meta']['total_count'])

    if count1 > 0:
        oc.add(DirectoryObject(
            key=Callback(albums.HandleAlbums, title=unicode(L('Albums')) + " " + title, artists=id),
            title=unicode(L('Albums') + ' (' + str(count1) + ')'),
            thumb=thumb
        ))

    response2 = service.get_tracks(artists=id, limit=1, offset=0,
                                         year__gte=common.get_start_music_year(),
                                         year__lte=common.get_end_music_year())
    count2 = int(response2['meta']['total_count'])

    if count2 > 0:
        oc.add(DirectoryObject(
            key=Callback(audio_tracks.HandleAudioTracks, name=L('Audio Tracks') + " " + title, thumb=thumb, artists=id),
            title=unicode(L('Audio Tracks') + ' (' + response2['meta']['total_count'] + ')'),
            thumb=thumb
        ))

    music_queue.append_controls(oc, name=title, artists=id, thumb=thumb)

    return oc

def add_search_artists(oc):
    oc.add(InputDirectoryObject(
        key=Callback(SearchMusicArtists, title=unicode(L("Artists Search"))),
        title=unicode(L("Artists Search")),
        thumb=R(SEARCH_ICON)
    ))
