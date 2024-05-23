def decode_hgetall(fetch: dict | None):
    return {x.decode(): fetch[x].decode() for x in fetch}
