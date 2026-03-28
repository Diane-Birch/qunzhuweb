import zlib, pathlib
sha='aadb960955ac4d059ff448e33b28a5c38263b4af'
p=pathlib.Path('.git/objects')/sha[:2]/sha[2:]
data=zlib.decompress(p.read_bytes())
print(repr(data[:120]))
