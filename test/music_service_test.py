# -*- coding: utf-8 -*-

import test_helper

import unittest
import json

from music_service import MusicService

class MuzarbuzServiceTest(unittest.TestCase):
    def setUp(self):
        self.service = MusicService()

    def test_get_albums(self):
        result = self.service.get_albums(limit=20)

        print(json.dumps(result, indent=4))
        print(len(result['objects']))

    def test_get_album_container(self):
        result = self.service.get_albums(parent_id=14485)

        print(json.dumps(result, indent=4))
        print(len(result['objects']))

    def test_get_albums_by_year_range(self):
        result = self.service.get_albums(year__gte=2014, year__lte=2015)

        print(json.dumps(result, indent=4))
        print(len(result['objects']))

    def test_get_artist_tracks(self):
        result = self.service.get_tracks(artists=1543)

        print(json.dumps(result, indent=4))
        print(len(result['objects']))

    def test_get_album_tracks(self):
        result = self.service.get_tracks(album=14486)

        print(json.dumps(result, indent=4))
        print(len(result['objects']))

    def test_get_collection_tracks(self):
        result = self.service.get_tracks(collection__id=115)

        print(json.dumps(result, indent=4))
        print(len(result['objects']))

    def test_get_artists(self):
        result = self.service.get_artists()

        print(json.dumps(result, indent=4))
        print(len(result['objects']))

    # def test_get_artist(self):
    #     result = self.service.get_artist(id=1543)
    #
    #     print(json.dumps(result, indent=4))

    def test_get_artists_annotated(self):
        result = self.service.get_artist_annotated(title__istartswith='В')

        print(json.dumps(result, indent=4))
        print(len(result['objects']))

    def test_get_collections(self):
        result = self.service.get_collections(limit=25)

        print(json.dumps(result, indent=4))
        print(len(result['objects']))

    # def test_get_collection(self):
    #     result = self.service.get_collection(id=115)
    #
    #     print(json.dumps(result, indent=4))

    def test_get_genres(self):
        result = self.service.get_genres()

        print(json.dumps(result, indent=4))
        print(len(result['objects']))

    def test_get_albums_by_genres(self):
        result = self.service.get_albums(genre__in=1)

        print(json.dumps(result, indent=4))
        print(len(result['objects']))

    def test_search(self):
        result = self.service.search(q='макаревич')

        for key, value in result.iteritems():
            print("For " + key + ":")
            if key == 'audio_track':
                print(json.dumps(value, indent=4))

            print(len(value['objects']))

if __name__ == '__main__':
    unittest.main()
