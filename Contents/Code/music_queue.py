import constants

def append_controls(oc, name, thumb=None, **params):
    type = get_type(params)
    id = params[type]

    if item_already_added_to_storage(type, id):
        oc.add(DirectoryObject(
                key=Callback(HandleRemoveFromQueue, type=type, id=id, name=name, thumb=thumb, **params),
                title=unicode(L('Remove from Queue')),
                thumb=R(constants.REMOVE_ICON)
        ))
    else:
        oc.add(DirectoryObject(
                key=Callback(HandleAddToQueue, type=type, id=id, name=name, thumb=thumb, **params),
                title=unicode(L('Add to Queue')),
                thumb=R(constants.ADD_ICON)
        ))
