def decode_hgetall(fetch: dict | None):
    if fetch is None:
        return None
    return { x.decode(): fetch[x].decode() for x in fetch }
