import requests
import json
from bs4 import BeautifulSoup

base_url = 'https://online.metro-cc.ru/category/chaj-kofe-kakao'

class MetroParser:
    """
    Parser object that parses all items from one category at online.metro-cc.ru website for two cities
    """
    cities_headers = {
        "Saint Petersburg" : {
            "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            'Connection' : 'keep-alive',
            "Cookie" : 'active_order=0; _slid_server=662a604494dd7c7d5c047fe5; metro_user_id=9ef82455103cf5be216da8f2dca976c8; _slid=662a604494dd7c7d5c047fe5; _ym_uid=1714053197589546476; _ym_d=1714053197; mindboxDeviceUUID=9800340d-3731-48a9-9713-0bdf67e9eb45; directCrm-session=%7B%22deviceGuid%22%3A%229800340d-3731-48a9-9713-0bdf67e9eb45%22%7D; tmr_lvid=e88b839735942155732d62d6679f6082; tmr_lvidTS=1714053196967; uxs_uid=2b38a1b0-030b-11ef-ba9f-dd34365e5ad6; metro_api_session=izgg4WwXlqXM1Q69xRyNsc8NFKFj8FEzAqF5hALT; _ym_isad=1; mp_selected_item={"promo_url":"https://online.metro-cc.ru/category/chaj-kofe-kakao/chay","promo_name":"Ð§Ð°Ð¹"}; _ga=GA1.1.1698873053.1714175246; _gcl_au=1.1.892424844.1714175246; metroStoreId=16; _slsession=8D7A7A3D-6097-4AE8-B59E-773F0A840CBB; _ym_visorc=w; _slfreq=633ff97b9a3f3b9e90027740%3A633ffa4c90db8d5cf00d7810%3A1714187957%3B64a81e68255733f276099da5%3A64abaf645c1afe216b0a0d38%3A1714187957; mp_5e1c29b29aeb315968bbfeb763b8f699_mixpanel=%7B%22distinct_id%22%3A%20%22%24device%3A18f15882beb3724-0baf3d821c40ac-1b525637-13c680-18f15882beb3724%22%2C%22%24device_id%22%3A%20%2218f15882beb3724-0baf3d821c40ac-1b525637-13c680-18f15882beb3724%22%2C%22%24search_engine%22%3A%20%22google%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fdocs.google.com%2F%22%2C%22%24initial_referring_domain%22%3A%20%22docs.google.com%22%2C%22__mps%22%3A%20%7B%7D%2C%22__mpso%22%3A%20%7B%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fdocs.google.com%2F%22%2C%22%24initial_referring_domain%22%3A%20%22docs.google.com%22%7D%2C%22__mpus%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpr%22%3A%20%5B%5D%2C%22__mpap%22%3A%20%5B%5D%7D; mp_88875cfb7a649ab6e6e310368f37a563_mixpanel=%7B%22distinct_id%22%3A%20%22%24device%3A18f15882c7037aa-0ace224d78e364-1b525637-13c680-18f15882c7037aa%22%2C%22%24device_id%22%3A%20%2218f15882c7037aa-0ace224d78e364-1b525637-13c680-18f15882c7037aa%22%2C%22%24search_engine%22%3A%20%22google%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fdocs.google.com%2F%22%2C%22%24initial_referring_domain%22%3A%20%22docs.google.com%22%2C%22__mps%22%3A%20%7B%7D%2C%22__mpso%22%3A%20%7B%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fdocs.google.com%2F%22%2C%22%24initial_referring_domain%22%3A%20%22docs.google.com%22%7D%2C%22__mpus%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpr%22%3A%20%5B%5D%2C%22__mpap%22%3A%20%5B%5D%7D; _ga_VHKD93V3FV=GS1.1.1714178663.2.1.1714180765.0.0.0'        
            },
        "Moscow" : {
            "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            'Connection' : 'keep-alive'
            }
    }

    def __init__(self, base_url):
        self._base_url = base_url

    def _create_subcat_dict(self):
        """
        Finds all subcategories to visit their links in future
        """
        print("URL:", self._base_url)
        with requests.get(self._base_url, headers=self._curr_headers) as response:
            print("\tStatus:", response.status_code)
            if response.status_code == 200:
                html = response.text
                soup = BeautifulSoup(html, 'lxml')
                subcat_class = "catalog-heading-link reset-link slider-main-block__heading-link style--catalog-1-level-products"
                for tag in soup.find_all("a", class_=subcat_class):
                    self._subcat_dict[ tag['href'].split("/")[-1] ]= []
            else:
                print("\tAn Error occured")

    def _fill_dict_with_items(self):
        """
        Starts creating dictionary: goes through every subcategory, looking for page counter and visits all the pages
        """
        for subcat in self._subcat_dict.keys():
            subcat_url = f"{base_url}/{subcat}"
            print("URL:", subcat_url)
            with requests.get(subcat_url, headers=self._curr_headers) as response:
                print("\tStatus:", response.status_code)
                if response.status_code == 200:
                    html = response.text
                    soup = BeautifulSoup(html, 'lxml')
                    pagination_item_class = "v-pagination__item catalog-paginate__item"
                    page_buttons = soup.find_all("a", class_=pagination_item_class)
                    pages_total = int(page_buttons[-1].text) if page_buttons else 1
                    for page in range(1, pages_total + 1):
                        self._add_items_from_page(url=f"{subcat_url}?page={page}", subcat_name=subcat)
                else:
                    print("\tAn Error occured")

    def _add_items_from_page(self, url, subcat_name):
        """
        Adds all items from page in dictionary
        """
        with requests.get(url, headers=self._curr_headers) as response:
            print("URL:", url)  
            print("\tStatus:", response.status_code)
            if response.status_code == 200:
                html = response.text
                soup = BeautifulSoup(html, 'lxml')
                print("\tAdress:", soup.find("button", class_='header-address__receive-button offline').text.strip())
                item_classes = ('catalog-2-level-product-card product-card subcategory-or-type__products-item with-prices-drop',
                                'catalog-2-level-product-card product-card subcategory-or-type__products-item with-prices-drop has-online-range-prices')
                for item_class in item_classes:
                    for tag in soup.find_all("div", class_=item_class):
                        self._subcat_dict[subcat_name].append(self._get_item(subcat_url=self._base_url+"/"+subcat_name, 
                                                                             soup=tag))
            else:
                print("\tAn Error occured")

    def _get_item(self, subcat_url, soup:BeautifulSoup) -> dict:
        """
        Creates dictionary with all information for single item
        """
        item_dict = dict()
        item_dict["ID"] = soup["id"]
        item_dict["Name"] = soup.find("span", class_="product-card-name__text").text.strip()
        item_dict["URL"] = subcat_url + \
            soup.find("a", class_="product-card-name reset-link catalog-2-level-product-card__name style--catalog-2-level-product-card")["href"]
        regular_price_html = soup.find("div", class_="product-unit-prices__old-wrapper")\
                                 .find("span", class_="product-price__sum-rubles")
        promo_price_html = soup.find("div", class_="product-unit-prices__actual-wrapper")\
                          .find("span", class_="product-price__sum-rubles")
        if regular_price_html:
            item_dict["Regular price"] = regular_price_html.text.replace("\u00a0", '')
            item_dict["Promo price"] = promo_price_html.text.replace("\u00a0", '')
        else:
            item_dict["Regular price"] = promo_price_html.text.replace("\u00a0", '')
            item_dict["Promo price"] = None
        return item_dict

    def create_json(self):
        """
        Creates json file with items for two cities to project root folder
        """
        final_dict = {}
        main_cat = self._base_url.split("/")[-1]
        for city in self.cities_headers.keys():
            self._curr_headers = self.cities_headers[city]
            self._subcat_dict = dict()
            self._create_subcat_dict()
            self._fill_dict_with_items()
            city_dict = {main_cat : self._subcat_dict}
            final_dict[city] = city_dict
        with open(f'metro-{main_cat}.json', 'w') as file:
            file.write(json.dumps(final_dict))
        
def main():
    parser = MetroParser(base_url)
    parser.create_json()

if __name__ == "__main__":
    main()
