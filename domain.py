import requests
from bs4 import BeautifulSoup
import math

BASE_URL = "https://www.commercialrealestate.com.au"

SUBURBS = "4704%2C33414%2C37664"
PROPERTY_TYPES = "125%2C233"
MIN_PRICE = "1000000"
MAX_PRICE = "3000000"
MIN_AREA = "750"
MAX_AREA = "3000"
MAP_AREA = "-27.44268%2C-27.66731%2C153.3138%2C152.93786%2C15"

def get_properties_per_page(url, page):
    print(f"[domain.com.au] Extracting properties in page {page}...")

    response = requests.get(f"{url}&pn={page}")
    soup = BeautifulSoup(response.text, "html.parser")

    container = soup.find("ul", {"data-testid": "search-results__card-container"})
    property_cards = container.find_all("li", recursive=False)

    properties = []

    for property_card in property_cards:
        image = property_card.find("picture").find("img")["src"]

        price = property_card.find("td", {"data-testid": "price"}).get_text()

        address_container = property_card.find("a", {"data-testid": "address"})
        sub_link = address_container["href"]
        link = f"{BASE_URL}{sub_link}"
        address = address_container.contents

        size = property_card.find("span", {"data-testid": "area-size"}).get_text()
        property_type = property_card.find("span", {"data-testid": "main-category"}).get_text()

        properties.append({
            "image": "",
            "suburb": address[2],
            "address": address[0],
            "price": price,
            "size": size,
            "type": property_type,
            "link": link,
            "image_link": image
        })

    return properties


def get_last_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    last_page = soup.find("div", {"data-testid": "pagination-text"}).get_text()
    last_page = last_page.replace("Page 1 of ", "")

    try:
        last_page = int(last_page)
    except:
        last_page = 1

    return last_page

def get_properties():
    properties = []

    url = f"{BASE_URL}/for-sale/?bb={MAP_AREA}&pt={PROPERTY_TYPES}&pr={MIN_PRICE}%2C{MAX_PRICE}&ls={MIN_AREA}%2C{MAX_AREA}"

    last_page = get_last_page(url)

    for page in range(int(last_page)):
        page += 1
        properties += get_properties_per_page(url, page)

    return properties
