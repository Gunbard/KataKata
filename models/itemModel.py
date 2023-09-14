import base64
import uuid
from json import JSONEncoder, JSONDecoder
from PyQt5 import QtCore
from retrievers.imageRetriever import ImageRetriever
from PyQt5.QtGui import QPixmap

class ItemModel:
  def __init__(self, name, description, image_url, upc, note, uid):
    self.name = name
    self.description = description
    self.image_url = image_url
    self.image = None
    self.upc = upc
    self.note = note
    self.uid = uid

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
  
  def generateUuid(self):
    self.uid = str(uuid.uuid4())

  def serializedImage(self):
    if not self.image:
      return None
    ba = QtCore.QByteArray()
    buffer = QtCore.QBuffer(ba)
    buffer.open(QtCore.QIODevice.WriteOnly)
    self.image.save(buffer, 'PNG')
    base64_data = ba.toBase64()
    return bytes(base64_data).decode('ascii')

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
    item = ItemModel(obj.get('name'), obj.get('description'), obj.get('image_url'), obj.get('upc'), obj.get('note'), obj.get('uid'))
    if not obj.get('image'):
      return item
    pixmap = QPixmap()
    pixmap.loadFromData(base64.b64decode(obj.get('image')))
    item.image = pixmap
    return item
