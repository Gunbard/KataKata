import json
import os
from models.itemModel import ItemModelJSONEncoder, ItemModelJSONDecoder

class CatalogModel:
  def __init__(self, data, filepath):
    # List of ItemModels
    self.data = data

    # String path to the save file
    self.filepath = filepath

  def getTitle(self):
    if self.filepath:
      return os.path.splitext(os.path.basename(self.filepath))[0]
    else:
      return ''

  def save(self):
    if not self.filepath or not self.data:
      return

    # Serialize data
    serializedData = json.dumps(self.data, cls=ItemModelJSONEncoder)
    file = open(self.filepath, 'w')
    file.write(serializedData)

  def load(self):
    if not self.filepath:
      return

    file = open(self.filepath, 'r')
    data = json.loads(file.read(), cls=ItemModelJSONDecoder)
    if data:
      self.data = data
