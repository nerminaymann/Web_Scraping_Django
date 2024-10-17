from itertools import product
import requests
from bs4 import BeautifulSoup
from core.models import Product

class WebScraper:
    def __init__(self,base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        self.LANGUAGE = "en-US,en;q=0.5"

    def setup_session(self):
        self.session.headers['User-Agent'] = self.USER_AGENT
        self.session.headers['Accept-Language'] = self.LANGUAGE
        self.session.headers['Content-Language'] = self.LANGUAGE

    def fetch_html_content(self, query):
        self.setup_session()
        response = self.session.get(f"{self.base_url}/catalog/?q={query}")
        response.raise_for_status() # to ensure the request is successful
        return response.text

class ProductParser(WebScraper):
    def __init__(self, base_url, product):
        super().__init__(base_url)
        self.product = product
        self.html_content = self.fetch_html_content(product)
        self.soup = BeautifulSoup(self.html_content, 'html.parser')

    def parse_products(self):
        products = self.soup.find_all('article', class_='prd _fb col c-prd')
        products_list = []
        for product in products:
            parsed_product = self._extract_product_data(product)
            if parsed_product:
                products_list.append(parsed_product)
        return products_list

    def _extract_product_data(self,product):
        img_c_div = product.find('div', class_='img-c')
        img_tag = img_c_div.find('img', class_='img') if img_c_div else None
        name_tag = product.find('h3', class_='name')
        new_price_tag = product.find('div', class_='prc')
        old_price_s_prc_w_div = product.find('div', class_='s-prc-w')
        old_price_tag = old_price_s_prc_w_div.find('div', class_='old') if old_price_s_prc_w_div else None
        discount_on_old_price_tag = old_price_s_prc_w_div.find('div', class_='bdg _dsct _sm') if old_price_s_prc_w_div else None
        stars_div = product.find('div', class_='stars _s')
        ratings_tag = stars_div.find('div', class_='in') if stars_div else None

        if img_tag and name_tag and new_price_tag:
            img_url = img_tag['data-src'] if img_tag else None
            name = name_tag.text
            new_price = new_price_tag.text
            old_price = old_price_tag.text if old_price_tag else None
            discount_on_old_price = discount_on_old_price_tag.text if discount_on_old_price_tag else None
            if ratings_tag:
                ratings_style = ratings_tag['style']
                width_value = ratings_style.split(':')[1].replace('%', '').strip()
                ratings = f'{float(width_value) / 20:.1f}'
            else:
                ratings = '0.0'
            product_instance = Product.objects.create(
                    name=name,
                    img_url=img_url,
                    new_price=new_price,
                    old_price=old_price,
                    discount=discount_on_old_price,
                    ratings=float(ratings)
                )
            product_instance.save()  # This will trigger the custom save method
            return product_instance
            # product_info = {
            #     "img_url": img_url, 'name': name, 'new_price': new_price, 'old_price': old_price,
            #     'discount': discount_on_old_price, 'ratings': ratings
            # }
            # return product_info
        return None