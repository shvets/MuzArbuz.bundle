import common
import albums
import artists
import audio_tracks
from music_info import MusicInfo

def append_controls(oc, name, thumb=None, **params):
    type = get_type(params)
    id = params[type]

    if item_already_added_to_storage(type, id):
        oc.add(DirectoryObject(
                key=Callback(HandleRemoveFromQueue, type=type, id=id, name=name, thumb=thumb, **params),
                title=unicode(L('Remove from Queue')),
                thumb=R(REMOVE_ICON)
        ))
    else:
        oc.add(DirectoryObject(
                key=Callback(HandleAddToQueue, type=type, id=id, name=name, thumb=thumb, **params),
                title=unicode(L('Add to Queue')),
                thumb=R(ADD_ICON)
        ))

@route('/music/music/add_to_queue')
def HandleAddToQueue(name, thumb, **params):
    type = get_type(params)
    id = params[type]

    music_info = MusicInfo(type=type, id=id, name=name, thumb=thumb)

    service.music_queue.add(music_info)
    service.music_queue.save()

    return ObjectContainer(
        header=u'%s' % L(name),
        message=u'%s' % L('Media Added')
    )

@route('/music/music/remove_from_queue')
def HandleRemoveFromQueue(name, thumb, **params):
    type = get_type(params)
    id = params[type]

    music_info = MusicInfo(type=type, id=id, name=name, thumb=thumb)

    service.music_queue.remove(music_info)
    service.music_queue.save()

    return ObjectContainer(
        header=u'%s' % L(name),
        message=u'%s' % L('Media Removed')
    )

@route('/music/music/queue')
def GetQueue(title, filter=None):
    oc = ObjectContainer(title2=unicode(L(title)))

    for media in service.music_queue.data:
        type = media['type']

        if type == filter:
            id = media['id']
            name = media['name']

            if 'thumb' in media:
                thumb = media['thumb']
            else:
                thumb = 'thumb'

            if filter == 'audio_tracks':
                key = Callback(audio_tracks.HandleAudioTracks, album=id, name=name, thumb=thumb)
                oc.add(DirectoryObject(key=key, title=unicode(name), thumb=thumb))
            elif filter == 'album':
                key = Callback(audio_tracks.HandleAudioTracks, album=id, name=name, thumb=thumb)
                oc.add(DirectoryObject(key=key, title=unicode(name), thumb=thumb))
            elif filter == 'artists':
                key=Callback(artists.GetArtistMenu, id=id, title=L(name), thumb=thumb)
                oc.add(DirectoryObject(key=key, title=unicode(L(name)), thumb=thumb
            ))
            elif filter == 'collection__id':
                key = Callback(audio_tracks.HandleAudioTracks, collection__id=id, name=name, thumb=thumb)
                oc.add(DirectoryObject(key=key, title=unicode(name), thumb=thumb))
            elif filter == 'genre__in':
                key = Callback(albums.HandleAlbums, title=name, genre__in=id)
                oc.add(DirectoryObject(key=key, title=unicode(name)))
            elif filter == 'parent__id':
                key = Callback(albums.HandleDoubleAlbum, name=name, parent__id=id, thumb=thumb)
                oc.add(DirectoryObject(key=key, title=unicode(name), thumb=thumb))

    common.add_search_music(oc)

    return oc

def get_type(params):
    if 'album' in params:
        type = 'album'
    elif 'collection__id' in params:
        type = 'collection__id'
    elif 'artists' in params:
        type = 'artists'
    elif 'audio_tracks' in params:
        type = 'audio_tracks'
    elif 'genre__in' in params:
        type = 'genre__in'
    elif 'parent__id' in params:
        type = 'parent__id'
    else:
        type = None

    return type

def item_already_added_to_storage(type, id):
    added = False

    for media in service.music_queue.data:
        if id == media['id']:
            added = True
            break

    return added