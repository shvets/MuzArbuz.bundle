ART = 'art-default.jpg'
ICON = 'icon-default.png'
SEARCH_ICON = 'icon-search.png'
OPTIONS_ICON = 'icon-options.png'
NEXT_ICON = 'icon-next.png'
BACK_ICON = 'icon-back.png'
ADD_ICON = 'icon-add.png'
REMOVE_ICON = 'icon-remove.png'

from plex_music_service import PlexMusicService

def on_error(e):
    Log(e)

    return ObjectContainer(header='Results', message=unicode(e))

service = PlexMusicService(on_error)

import common
import albums
import artists
import collections
import genres
import audio_tracks

def Start(): # Initialize the plug-in
    HTTP.CacheTime = CACHE_1HOUR

    common.validate_prefs()

@handler('/music/music', 'Muzarbuz', thumb=ICON, art=ART)
def MainMenu(complete=False, offline=False):
    oc = ObjectContainer(title1='Muzarbuz', art=R(ART))

    oc.http_cookies = HTTP.CookiesForURL(service.API_URL)

    oc = ObjectContainer(title2=unicode(L('Music')))

    oc.add(DirectoryObject(key=Callback(albums.GetAlbumsMenu, title=L('Albums')), title=unicode(L('Albums'))))
    oc.add(DirectoryObject(key=Callback(artists.GetArtistsMenu, title=L('Artists')), title=unicode(L('Artists'))))
    oc.add(DirectoryObject(key=Callback(collections.GetCollectionsMenu, title=L('Collections')), title=unicode(L('Collections'))))
    oc.add(DirectoryObject(key=Callback(genres.GetGenresMenu, title=L('Genres')), title=unicode(L('Genres'))))

    common.add_search_music(oc)

    return oc
