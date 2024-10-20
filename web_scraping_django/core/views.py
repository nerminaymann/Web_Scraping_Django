import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from django.views.generic import TemplateView

from core.services.scraper_service import WebScraper, ProductParser

class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products_list_info = []

        if 'product' in self.request.GET:
            product_query = self.request.GET.get('product')
            base_url = "https://www.jumia.com.eg"

            # Parse the product data
            parser = ProductParser(base_url, product_query)
            products_list_info = parser.parse_products()

        context['products_list_info'] = products_list_info
        return context