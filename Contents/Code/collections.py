import common
import music_queue
import pagination
import artists
import audio_tracks

@route('/music/music/collections_menu')
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

@route('/music/music/collections')
def HandleCollections(title, page=1, **params):
    oc = ObjectContainer()

    page = int(page)
    limit = common.get_elements_per_page()
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

    common.add_pagination_to_response(response, page)
    pagination.append_controls(oc, response, callback=HandleCollections, title=title, page=page)

    return oc

@route('/music/music/collection')
def HandleCollection(title, collection__id, thumb):
    oc = ObjectContainer(title2=unicode(L(title)))

    key = Callback(audio_tracks.HandleAudioTracks, name=title, collection__id=collection__id, thumb=thumb)
    oc.add(DirectoryObject(key=key, title=unicode(title), thumb=thumb))

    music_queue.append_controls(oc, name=title, thumb=thumb, collection__id=collection__id)

    return oc

@route('/music/music/search_music_collections')
def SearchMusicCollections(title, query, page=1, **params):
    page = int(page)
    limit = common.get_elements_per_page()
    offset = (page-1)*limit

    oc = ObjectContainer(title2=unicode(L(title)))

    response = service.search_collection(q=query, limit=common.get_elements_per_page(), offset=offset)

    for media in artists.BuildArtistsList(response['objects']):
        oc.add(media)

    common.add_pagination_to_response(response, page)
    pagination.append_controls(oc, response, callback=SearchMusicCollections, title=title, query=query, page=page, **params)

    return oc

def add_search_collections(oc):
    oc.add(InputDirectoryObject(
        key=Callback(SearchMusicCollections, title=unicode(L("Collections Search"))),
        title=unicode(L("Collections Search")),
        thumb=R(SEARCH_ICON)
    ))