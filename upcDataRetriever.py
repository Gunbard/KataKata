import requests
from bs4 import BeautifulSoup

class UpcDataRetriever:
    RESOURCE_URL = "https://go-upc.com/search?q={}"

    def __init__(self, upc):
        self.upc = upc

    def get(self):
        if self.upc is None:
            return None

        print(self.upc)

        response = requests.get(self.RESOURCE_URL.format(self.upc))
        soup = BeautifulSoup(response.text, 'html.parser')

        title_element = soup.find('h1', {'class': 'product-name'})
        title = title_element.text if title_element else None

        if not title:
            return None

        image_url = soup.find('img')['src']
        description = soup.find('h2').parent.find('span').text.strip()

        type_element = soup.find(text='Type:')
        type = type_element.parent.parent.text.replace('Type: ', '') if type_element else None

        print(title)
        print(image_url)
        print(description)
        print(type)

        return {
            'title': title, 
            'image_url': image_url, 
            'description': description, 
            'type': type
        }