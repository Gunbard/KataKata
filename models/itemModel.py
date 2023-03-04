from retrievers.imageRetriever import ImageRetriever

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