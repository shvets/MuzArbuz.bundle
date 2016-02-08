import common
import music_queue
import albums

@route('/music/music/genres_menu')
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

    common.add_search_music(oc)

    return oc

@route('/music/music/music_genres')
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

    common.add_search_music(oc)

    return oc

@route('/music/music/music_genre')
def HandleMusicGenre(title, genre__in, thumb):
    oc = ObjectContainer(title2=unicode(L(title)))

    key = Callback(albums.HandleAlbums, title=title, genre__in=genre__in)
    oc.add(DirectoryObject(key=key, title=unicode(title)))

    music_queue.append_controls(oc, name=title, thumb=thumb, genre__in=genre__in)

    common.add_search_music(oc)

    return oc