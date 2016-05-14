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

    oc.add(DirectoryObject(key=Callback(HandleAlbumsMenu, title=L('Albums')), title=unicode(L('Albums'))))
    oc.add(DirectoryObject(key=Callback(HandleArtistsMenu, title=L('Artists')), title=unicode(L('Artists'))))
    oc.add(DirectoryObject(key=Callback(HandleCollectionsMenu, title=L('Collections')), title=unicode(L('Collections'))))
    oc.add(DirectoryObject(key=Callback(HandleGenresMenu, title=L('Genres')), title=unicode(L('Genres'))))

    oc.add(InputDirectoryObject(key=Callback(main.HandleSearch), title=unicode(L("Search Music")),
                                thumb=R(constants.SEARCH_ICON)))

    return oc

@route(constants.PREFIX + '/albums_menu')
def HandleAlbumsMenu(title):
    oc = ObjectContainer(title2=unicode(L(title)))

    oc.add(DirectoryObject(
            key=Callback(main.HandleAlbums, title=L('All Albums')),
            title=unicode(L('All Albums'))
    ))

    oc.add(DirectoryObject(
            key=Callback(main.HandleQueue, filter='album'),
            title=unicode(L('Favorite Albums'))))

    oc.add(DirectoryObject(
            key=Callback(main.HandleQueue, filter='double_album'),
            title=unicode(L('Favorite Double Albums'))))

    oc.add(InputDirectoryObject(
            key=Callback(main.SearchAlbums, title=unicode(L("Albums Search"))),
            title=unicode(L("Albums Search")),
            thumb=R(constants.SEARCH_ICON)
    ))

    return oc

@route(constants.PREFIX + '/artists_menu')
def HandleArtistsMenu(title):
    oc = ObjectContainer(title2=unicode(L(title)))

    oc.add(DirectoryObject(
            key=Callback(main.HandleArtists, title=L('All Artists')),
            title=unicode(L('All Artists'))
    ))
    oc.add(DirectoryObject(
            key=Callback(main.GetCyrillicLettersMenu, title=L('By Letter')),
            title=unicode(L('By Letter'))
    ))
    oc.add(DirectoryObject(
            key=Callback(main.GetLatinLettersMenu, title=L('By Latin Letter')),
            title=unicode(L('By Latin Letter'))
    ))
    oc.add(DirectoryObject(
            key=Callback(main.HandleArtists, title=L('Favorite Artists')),
            title=unicode(L('Favorite Artists'))
    ))

    oc.add(InputDirectoryObject(
        key=Callback(main.SearchArtists, title=unicode(L("Artists Search"))),
        title=unicode(L("Artists Search")),
        thumb=R(constants.SEARCH_ICON)
    ))

    return oc

@route(constants.PREFIX + '/collections_menu')
def HandleCollectionsMenu(title):
    oc = ObjectContainer(title2=unicode(L(title)))

    oc.add(DirectoryObject(
            key=Callback(main.HandleCollections, title=L('All Collections')),
            title=unicode(L('All Collections'))
    ))
    oc.add(DirectoryObject(
            key=Callback(main.HandleQueue, title=L('Favorite Collections')),
            title=unicode(L('Favorite Collections'))
    ))

    oc.add(InputDirectoryObject(
        key=Callback(main.SearchCollections, title=unicode(L("Collections Search"))),
        title=unicode(L("Collections Search")),
        thumb=R(constants.SEARCH_ICON)
    ))

    return oc

@route(constants.PREFIX + '/genres_menu')
def HandleGenresMenu(title):
    oc = ObjectContainer(title2=unicode(L(title)))

    oc.add(DirectoryObject(
            key=Callback(main.HandleGenres, title=L('All Genres')),
            title=unicode(L('All Genres'))
    ))

    oc.add(DirectoryObject(
            key=Callback(main.HandleQueue, title=L('Favorite Genres')),
            title=unicode(L('Favorite Genres'))
    ))

    oc.add(InputDirectoryObject(key=Callback(main.HandleSearch), title=unicode(L("Search Music")),
                                thumb=R(constants.SEARCH_ICON)))

    return oc
