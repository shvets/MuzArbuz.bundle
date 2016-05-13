import constants

import util

util.add_library("common")

from muz_arbuz_plex_service import MuzArbuzPlexService

service = MuzArbuzPlexService()

import main

def Start():
    HTTP.CacheTime = CACHE_1HOUR

    util.validate_prefs()

@handler(constants.PREFIX, 'MuzArbuz', thumb=constants.ICON, art=constants.ART)
def MainMenu():
    oc = ObjectContainer(title1='MuzArbuz', art=R(constants.ART))

    oc.http_cookies = HTTP.CookiesForURL(service.API_URL)

    oc = ObjectContainer(title2=unicode(L('Music')))

    oc.add(DirectoryObject(key=Callback(main.GetAlbumsMenu, title=L('Albums')), title=unicode(L('Albums'))))
    oc.add(DirectoryObject(key=Callback(main.GetArtistsMenu, title=L('Artists')), title=unicode(L('Artists'))))
    oc.add(DirectoryObject(key=Callback(main.GetCollectionsMenu, title=L('Collections')), title=unicode(L('Collections'))))
    oc.add(DirectoryObject(key=Callback(main.GetGenresMenu, title=L('Genres')), title=unicode(L('Genres'))))

    main.add_search_music(oc)

    return oc
