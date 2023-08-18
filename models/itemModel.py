import base64
from json import JSONEncoder, JSONDecoder
from PyQt5 import QtCore
from retrievers.imageRetriever import ImageRetriever
from PyQt5.QtGui import QPixmap

class ItemModel:
  def __init__(self, name, description, image_url, upc, note):
    self.name = name
    self.description = description
    self.image_url = image_url
    self.image = None
    self.upc = upc
    self.note = note

  def refreshImage(self):
    if not self.image_url:
      return

    self.image = ImageRetriever(self.image_url).get()

  def imageThumbnail(self):
    if not self.image:
      return None
    
    return self.image.scaled(64, 64, \
                        QtCore.Qt.KeepAspectRatio, \
                        QtCore.Qt.SmoothTransformation)

class ItemModelJSONEncoder(JSONEncoder):
  def default(self, obj):
    if isinstance(obj, ItemModel):
      return obj.__dict__
    if isinstance(obj, QPixmap):
      ba = QtCore.QByteArray()
      buffer = QtCore.QBuffer(ba)
      buffer.open(QtCore.QIODevice.WriteOnly)
      obj.save(buffer, 'PNG')
      base64_data = ba.toBase64()
      return bytes(base64_data).decode('ascii')
    return JSONEncoder.default(self, obj)

class ItemModelJSONDecoder(JSONDecoder):
  def __init__(self, *args, **kwargs):
    JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

  def object_hook(self, obj):
    item = ItemModel(obj['name'], obj['description'], obj['image_url'], obj['upc'], obj['note'])
    if not obj['image']:
      return item
    pixmap = QPixmap()
    pixmap.loadFromData(base64.b64decode(obj['image']))
    item.image = pixmap
    return item
