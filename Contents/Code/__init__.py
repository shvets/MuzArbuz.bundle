import constants

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

@handler(constants.PREFIX, 'Muzarbuz', thumb=constants.ICON, art=constants.ART)
def MainMenu(complete=False, offline=False):
    oc = ObjectContainer(title1='Muzarbuz', art=R(constants.ART))

    oc.http_cookies = HTTP.CookiesForURL(service.API_URL)

    oc = ObjectContainer(title2=unicode(L('Music')))

    oc.add(DirectoryObject(key=Callback(albums.GetAlbumsMenu, title=L('Albums')), title=unicode(L('Albums'))))
    oc.add(DirectoryObject(key=Callback(artists.GetArtistsMenu, title=L('Artists')), title=unicode(L('Artists'))))
    oc.add(DirectoryObject(key=Callback(collections.GetCollectionsMenu, title=L('Collections')), title=unicode(L('Collections'))))
    oc.add(DirectoryObject(key=Callback(genres.GetGenresMenu, title=L('Genres')), title=unicode(L('Genres'))))

    common.add_search_music(oc)

    return oc
