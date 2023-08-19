import requests
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap

MAX_IMAGE_DIMENSION = 1080

class ImageRetriever:
  def __init__(self, url):
    self.url = url

  def get(self):
    if not self.url:
      return None
        
    response = requests.get(self.url, stream=True)
    pixmap = QPixmap()
    pixmap.loadFromData(response.raw.data)
    
    # Limit image dimensions
    if pixmap.width() > MAX_IMAGE_DIMENSION or pixmap.height() > MAX_IMAGE_DIMENSION:
      pixmap = pixmap.scaled(MAX_IMAGE_DIMENSION, MAX_IMAGE_DIMENSION, \
                      QtCore.Qt.KeepAspectRatio, \
                      QtCore.Qt.SmoothTransformation)

    return pixmap
    