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
                                 url_items=url_items, player=PlayMusic)

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
def PlayMusic(url):
    return Redirect(url)