import base64, pathlib
files=['frontend/src/App.vue','frontend/src/styles/base.css','frontend/src/views/SectionDetailView.vue','frontend/src/views/ProductDetailView.vue','frontend/src/views/NewsDetailView.vue']
for path in files:
    data=pathlib.Path(path).read_bytes()
    print('@@FILE@@ ' + path)
    print(base64.b64encode(data).decode('ascii'))
