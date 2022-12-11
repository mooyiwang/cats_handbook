def getcounts(dl, id):
    for c in dl:
        if c['c'] == id:
            return c['counts']
    return 0

