import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from core.services.scraper_service import WebScraper, ProductParser
def home(request):
    products_list_info = []
    if 'product' in request.GET:
        product_query = request.GET.get('product')
        base_url = "https://www.jumia.com.eg"

        # Parse the product data
        parser = ProductParser(base_url,product_query)
        products_list_info = parser.parse_products()

    return render(request, 'core/home.html', {'products_list_info': products_list_info})