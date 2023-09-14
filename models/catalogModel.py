import json
import os
from bs4 import BeautifulSoup, Tag
from datetime import datetime
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
    
  def getHTML(self):
    # TODO: Sorting options
    soup = BeautifulSoup()
    html = soup.new_tag("html")
    style = soup.new_tag("style")
    style.append("body { font-family: 'Georgia', serif; }\n" \
                 "img { max-width: 256px; max-height: 256px; }\n" \
                 ".item { padding: 16px; }\n" \
                 ".item div { padding: 8px; }\n" \
                 ".name {font-weight: bold; }\n")
    container = soup.new_tag("div")
    container.attrs['class'] = 'mainContainer'
    soup.append(html)
    html.append(style)
    html.append(container)
    header = soup.new_tag("div")
    header.attrs['class'] = 'header'
    now = datetime.now()
    title = soup.new_tag("div")
    title.attrs['class'] = 'catalogTitle'
    title.append(self.getTitle())
    count = soup.new_tag("div")
    count.attrs['class'] = 'itemCount'
    count.append("{} items".format(len(self.data)))
    header.append(title)
    header.append(count)
    header.append("Generated on {}.".format(now.strftime("%m/%d/%Y %I:%M:%S %p")))
    container.append(header)

    for item in self.data:
      newItem = soup.new_tag("div")
      newItem.attrs['class'] = 'item'
      
      newItemName = soup.new_tag("div")
      newItemName.attrs['class'] = 'name'
      newItemName.append(item.name) if item.name else ""
      newItem.append(newItemName)

      newItemUPC = soup.new_tag("div")
      newItemUPC.attrs['class'] = 'upc'
      newItemUPC.append(item.upc) if item.upc else ""
      newItem.append(newItemUPC)

      newItemDesc = soup.new_tag("div")
      newItemDesc.attrs['class'] = 'desc'
      newItemDesc.append(item.description) if item.description else ""
      newItem.append(newItemDesc)

      newItemNote = soup.new_tag("div")
      newItemNote.attrs['class'] = 'note'
      newItemNote.append(item.note) if item.note else ""
      newItem.append(newItemNote)

      if item.image:
        newItemImg = soup.new_tag("img")
        newItemImg.attrs['class'] = 'image'
        newItemImg.attrs['src'] = "data:image/png;base64," + item.serializedImage()
        newItem.append(newItemImg)
      
      container.append(newItem)

    return soup.prettify()

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
      # Generate uuids if they're blank
      for item in data:
        if not item.uid:
          item.generateUuid()

      self.data = data