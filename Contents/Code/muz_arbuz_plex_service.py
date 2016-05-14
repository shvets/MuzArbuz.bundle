from muz_arbuz_service import MuzArbuzService
from muz_arbuz_plex_storage import MuzArbuzPlexStorage

class MuzArbuzPlexService(MuzArbuzService):
     def __init__(self):
        storage_name = Core.storage.abs_path(Core.storage.join_path(Core.bundle_path, 'Contents', 'muzarbuz.storage'))

        self.queue = MuzArbuzPlexStorage(storage_name)

        self.queue.register_simple_type('album')
        self.queue.register_simple_type('double_album')
        self.queue.register_simple_type('artist')
        self.queue.register_simple_type('tracks')
