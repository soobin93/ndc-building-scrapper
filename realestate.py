import requests
from bs4 import BeautifulSoup
import math

BASE_URL = "https://www.realcommercial.com.au"

LOCATIONS = "brisbane-city-qld-4000, underwood-qld-4119, slacks-creek-qld-4127"

PROPERTY_TYPE = "industrial-warehouse"
MIN_AREA = "700"
MAX_AREA = "3000"
MIN_PRICE = "1000000"
MAX_PRICE = "3000000"
NUMBER_OF_PROPERTIES_PER_PAGE = 10

def get_properties_per_page(url, page):
    print(f"[realestate.com.au] Extracting properties in page {page}...")

    response = requests.get(f"{url}&page={page}")
    soup = BeautifulSoup(response.text, "html.parser")

    property_wrapper = soup.find("ol", {"class": "listings"})
    property_cards = property_wrapper.find_all("div", {"class": "ListingCard_listingCard_28qiR"})

    properties = []

    for property_card in property_cards:
        other_container = property_card.find("div", {"class": "OtherResultsBanner_textContainer_nIlNq"})

        if other_container is None:
            # Get Title
            headline = property_card.find("span", {"class": "Headlines_title_1NHme"})
            if headline is not None:
                title = headline.get_text()
            else:
                title = ""

            # Get Address
            address_wrapper = property_card.find("h2", {"class": "Address_wrapper_7yCHK"})
            address = address_wrapper.find("a", {"class": "Address_link_1aaSW"})["title"]

            # Get Price
            price = property_card.find("h3", {"class": "Price_price_1Q20z"}).get_text()

            # Get Size & Type
            attribute_container = property_card.find("div", {"class": "ListingAttributes_container_3BNJO"})
            attributes = attribute_container.find_all("span")

            size = attributes[0].get_text()
            property_type = attributes[1].get_text()

            # Get link
            link = address_wrapper.find("a")["href"]
            link = f"{BASE_URL}{link}"

            properties.append({
                "title": title,
                "address": address,
                "price": price,
                "size": size,
                "type": property_type,
                "link": link
            })

    return properties

def get_last_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    total_properties_count = soup.find("span", {"class": "SearchResultsHeader_availableResults_2ahBB"}).get_text()
    total_properties_count = total_properties_count.replace(" properties found", "")

    try:
        total_properties_count = int(total_properties_count)
    except:
        total_properties_count = 1

    return math.ceil(total_properties_count / NUMBER_OF_PROPERTIES_PER_PAGE)

def get_properties():
    properties = []

    url = f"{BASE_URL}/for-sale/{PROPERTY_TYPE}/?locations={LOCATIONS}&minSiteArea={MIN_AREA}&maxSiteArea={MAX_AREA}&minPrice={MIN_PRICE}&maxPrice={MAX_PRICE}"

    last_page = get_last_page(url)

    for page in range(int(last_page)):
        page += 1
        properties += get_properties_per_page(url, page)

    return properties
