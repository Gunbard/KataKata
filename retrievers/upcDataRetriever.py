import requests
from bs4 import BeautifulSoup
from models.itemModel import ItemModel

class UpcDataRetriever:
    RESOURCE_URL = "https://go-upc.com/search?q={}"

    def refresh(self, item):
        if item.upc is None:
            return None

        print(item.upc)

        response = requests.get(self.RESOURCE_URL.format(item.upc))
        soup = BeautifulSoup(response.text, 'html.parser')

        title_element = soup.find('h1', {'class': 'product-name'})
        title = title_element.text if title_element else None

        if not title:
            return None

        image_url = soup.find('img')['src']
        description = soup.find('h2').parent.find('span').text.strip()

        print(title)
        print(image_url)
        print(description)

        item.name = title
        item.description = description
        item.image_url = image_url
        item.refreshImage()