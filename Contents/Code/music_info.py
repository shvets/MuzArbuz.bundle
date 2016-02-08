class MusicInfo(dict):
    def __init__(self, type, id, name, thumb=None):
        super(MusicInfo, self).__init__()

        self['type'] = type
        self['id'] = id
        self['name'] = name
        self['thumb'] = thumb