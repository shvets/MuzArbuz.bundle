import common
import music_queue
import pagination

@route('/music/music/search_music_audio_tracks')
def SearchMusicAudioTracks(title, query, page, **params):
    oc = ObjectContainer(title2=unicode(L(title)))

    page = int(page)
    limit = common.get_elements_per_page()
    offset = (page-1)*limit

    response = service.search_audio_track(q=query, limit=common.get_elements_per_page(), offset=offset)

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

        oc.add(GetAudioTrack(title=unicode(title), thumb=thumb, artist=artist, format=format, url=url))

    common.add_pagination_to_response(response, page)
    pagination.append_controls(oc, response, callback=SearchMusicAudioTracks, title=title, query=query, page=page, **params)

    return oc

@route('/music/music/audio_tracks')
def HandleAudioTracks(name, thumb, page=1, **params):
    oc = ObjectContainer(title2=unicode(name))

    page = int(page)
    limit = common.get_elements_per_page()
    offset = (page-1)*limit

    response = service.get_tracks(limit=common.get_elements_per_page(), offset=offset, **params)

    for media in response['objects']:
        title = media['title']
        file = media['file']

        if media['album']['artist']:
            artist = media['album']['artist']['title']
        else:
            artist = ''

        format = 'mp3'
        url = service.BASE_URL + file

        oc.add(GetAudioTrack(title=unicode(title), thumb=thumb, artist=artist, format=format, url=url))

    music_queue.append_controls(oc, name=name, thumb=thumb, **params)

    common.add_pagination_to_response(response, page)
    pagination.append_controls(oc, response, callback=HandleAudioTracks, name=name, thumb=thumb, page=page, **params)

    return oc

@route('/music/music/audio_track')
def GetAudioTrack(title, thumb, artist, format, url, container=False, **params):
    track = MetadataObjectForURL(title=title, thumb=thumb, artist=artist, format=format, url=url, container=container)

    if container:
        oc = ObjectContainer(title2=unicode(title))

        oc.add(track)

        return oc
    else:
        return track

def MetadataObjectForURL(title, thumb, artist, format, url, container):
    track = TrackObject(
        key=Callback(GetAudioTrack, title=title, thumb=thumb, format=format, artist=artist, url=url, container=True),
        rating_key = unicode(title),
        title = unicode(title),
        # album = 'album',
        thumb=thumb,
        artist = artist
    )

    track.items = MediaObjectsForURL(url, format)

    return track

def MediaObjectsForURL(url, format):
    if 'm4a' in format:
        container = Container.MP4
        audio_codec = AudioCodec.AAC
    else:
        container = Container.MP3
        audio_codec = AudioCodec.MP3

    media_objects = []

    media_object = MediaObject(
        container = container,
        optimized_for_streaming=True
    )

    part_object = PartObject(key=Callback(PlayMusic, url=url))

    audio_stream = AudioStreamObject(codec=audio_codec, channels=2, bitrate=str(128))

    part_object.streams = [audio_stream]

    media_object.parts.append(part_object)

    media_objects.append(media_object)

    return media_objects

@route('/music/music/play_audio')
def PlayMusic(url):
    Log(url)

    return Redirect(url)