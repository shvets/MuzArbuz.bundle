from music_service import MusicService
from plex_storage import PlexStorage

class PlexMusicService(MusicService):
     def __init__(self):
        storage_name = Core.storage.abs_path(Core.storage.join_path(Core.bundle_path, 'Contents', 'music.storage'))

        self.music_queue = PlexStorage(storage_name)