import json
from models.itemModel import ItemModelJSONEncoder, ItemModelJSONDecoder

class CatalogModel:
  def __init__(self, data, filepath):
    # List of ItemModels
    self.data = data

    # String path to the save file
    self.filepath = filepath

  def save(self):
    if not self.filepath or not self.data:
      return

    # Serialize data
    serializedData = json.dumps(self.data, cls=ItemModelJSONEncoder)
    file = open(self.filepath, 'w')
    file.write(serializedData)

  def load(self):
    if not self.filepath:
      print('Error: No file to load!')
      return

    file = open(self.filepath, 'r')
    data = json.loads(file.read(), cls=ItemModelJSONDecoder)
    if data:
      self.data = data
