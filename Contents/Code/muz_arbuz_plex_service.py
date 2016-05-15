from muz_arbuz_service import MuzArbuzService
from plex_storage import PlexStorage

class MuzArbuzPlexService(MuzArbuzService):
    def __init__(self):
        storage_name = Core.storage.abs_path(Core.storage.join_path(Core.bundle_path, 'Contents', 'muzarbuz.storage'))

        self.queue = PlexStorage(storage_name)

        self.queue.register_simple_type('album')
        self.queue.register_simple_type('double_album')
        self.queue.register_simple_type('artist')
        self.queue.register_simple_type('collection')
        self.queue.register_simple_type('genre')
        self.queue.register_simple_type('tracks')

    def handle_bookmark_operation(self, operation, media_info):
        if operation == 'add':
            self.queue.add(media_info)
        elif operation == 'remove':
            self.queue.remove(media_info)

    def append_bookmark_controls(self, oc, handler, media_info):
        bookmark = self.queue.find(media_info)

        if bookmark:
            oc.add(DirectoryObject(
                key=Callback(handler, operation='remove', **media_info),
                title=unicode(L('Remove Bookmark')),
                thumb=R(constants.REMOVE_ICON)
            ))
        else:
            oc.add(DirectoryObject(
                key=Callback(handler, operation='add', **media_info),
                title=unicode(L('Add Bookmark')),
                thumb=R(constants.ADD_ICON)
            ))