# -*- coding: utf-8 -*-

import json

from http_service import HttpService

class MusicService(HttpService):
    BASE_URL = "https://muzarbuz.com"
    API_URL = BASE_URL + "/api/v1"

    USER_AGENT = 'Plex User Agent'

    def get_albums(self, **params):
        url = self.build_url(self.API_URL + "/album", **params)

        return self.api_request(url, **params)

    def get_tracks(self, **params):
        url = self.build_url(self.API_URL + "/audio_track", **params)

        return self.api_request(url, **params)

    def get_artists(self, **params):
        url = self.build_url(self.API_URL + "/artist", **params)

        return self.api_request(url, **params)

    # def get_artist(self, id):
    #     url = self.build_url(self.API_URL + "/artist/" + str(id))
    #
    #     return self.api_request(url, **params)

    def get_artist_annotated(self, **params):
        url = self.build_url(self.API_URL + "/artist_annotated", **params)

        return self.api_request(url, **params)

    def get_collections(self, **params):
        url = self.build_url(self.API_URL + "/collection", **params)

        return self.api_request(url, **params)

    # def get_collection(self, id):
    #     url = self.build_url(self.API_URL + "/collection/" + str(id))
    #
    #     return self.api_request(url, **params)

    def get_genres(self, **params):
        url = self.build_url(self.API_URL + "/genre", **params)

        return self.api_request(url, **params)

    def search(self, limit=0, offset=0, **params):
        return {
            'collection': self.search_collection(limit=limit, offset=offset, **params),
            'artist_annotated': self.search_artist_annotated(limit=limit, offset=offset, **params),
            'album': self.search_album(limit=limit, offset=offset, **params),
            'audio_track': self.search_audio_track(limit=limit, offset=offset, **params)
        }

    def search_collection(self, **params):
        url = self.build_url(self.API_URL + "/collection/search/", **params)

        return self.api_request(url, **params)

    def search_artist_annotated(self, **params):
        url = self.build_url(self.API_URL + "/artist_annotated/search/", **params)

        return self.api_request(url, **params)

    def search_album(self, **params):
        url = self.build_url(self.API_URL + "/album/search/", **params)

        return self.api_request(url, **params)

    def search_audio_track(self, **params):
        url = self.build_url(self.API_URL + "/audio_track/search/", **params)

        return self.api_request(url, **params)

    def api_request(self, url, **params):
        headers = {}

        headers['User-agent'] = self.USER_AGENT
        headers['Content-Type'] = 'application/json'

        return json.loads(self.http_request(url, headers=headers))