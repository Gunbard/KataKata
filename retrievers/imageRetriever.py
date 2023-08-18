import requests
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap

class ImageRetriever:
  def __init__(self, url):
    self.url = url

  def get(self):
    if not self.url:
      return None
        
    response = requests.get(self.url, stream=True)
    pixmap = QPixmap()
    pixmap.loadFromData(response.raw.data)
    return pixmap
    