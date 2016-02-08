import common
import pagination
import music_queue
import audio_tracks

@route('/music/music/albums_menu')
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
            thumb=R(SEARCH_ICON)
    ))

    return oc

@route('/music/music/search_music_albums')
def SearchMusicAlbums(title, query, page=1, **params):
    oc = ObjectContainer(title2=unicode(L(title)))

    page = int(page)
    limit = common.get_elements_per_page()
    offset = (page-1)*limit

    response = service.search_album(q=query, limit=common.get_elements_per_page(), offset=offset)

    for media in BuildAlbumsList(response['objects']):
        oc.add(media)

    common.add_pagination_to_response(response, page)
    pagination.append_controls(oc, response, callback=SearchMusicAlbums, title=title, query=query, page=page, **params)

    return oc

@route('/music/music/albums')
def HandleAlbums(title, page=1, **params):
    oc = ObjectContainer(title2=unicode(L(title)))

    page = int(page)
    limit = common.get_elements_per_page()
    offset = (page-1)*limit

    response = service.get_albums(limit=limit, offset=offset,
                                        year__gte=common.get_start_music_year(),
                                        year__lte=common.get_end_music_year(),
                                        **params)

    oc.title2 = unicode(L(title)) + ' (' + str(response['meta']['total_count']) + ')'

    for media in BuildAlbumsList(response['objects']):
        oc.add(media)

    oc.add(InputDirectoryObject(
            key=Callback(SearchMusicAlbums, title=unicode(L("Albums Search")), page=page),
            title=unicode(L("Albums Search")),
            thumb=R(SEARCH_ICON)
    ))

    common.add_pagination_to_response(response, page)
    pagination.append_controls(oc, response, callback=HandleAlbums, title=title, page=page, **params)

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
            key = Callback(audio_tracks.HandleAudioTracks, album=id, name=title, thumb=thumb, **params)
        elif music_container:
            key = Callback(HandleDoubleAlbum, parent__id=id, name=title, thumb=thumb, **params)
        else:
            key = Callback(audio_tracks.HandleAudioTracks, album=id, name=title, thumb=thumb, **params)

        list.append(DirectoryObject(key=key, title=unicode(title), thumb=thumb))

    return list

@route('/music/music/double_album')
def HandleDoubleAlbum(name, thumb, **params):
    oc = ObjectContainer(title2=unicode(name))

    response = service.get_albums(limit=common.get_elements_per_page(),
                                        year__gte=common.get_start_music_year(),
                                        year__lte=common.get_end_music_year(),
                                        **params)

    for media in response['objects']:
        id = media['id']
        title = media['title']
        thumb = media['thumbnail']

        key = Callback(audio_tracks.HandleAudioTracks, album=id, name=title, thumb=thumb)
        oc.add(DirectoryObject(key=key, title=unicode(title), thumb=thumb))

    music_queue.append_controls(oc, name=name, thumb=thumb, **params)

    return oc
