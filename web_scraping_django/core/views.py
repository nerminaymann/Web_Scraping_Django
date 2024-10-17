import requests
from bs4 import BeautifulSoup
from django.shortcuts import render

#to return html content after scraping the web page
def get_content(product):
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html_content = session.get(f'https://www.jumia.com.eg/catalog/?q={product}').text
    return html_content

def home(request):
    products_list_info = []
    if 'product' in request.GET:
        product = request.GET.get('product')    
        html_content = get_content(product)
        #to beautify the html content
        soup = BeautifulSoup(html_content, 'html.parser')
        products = soup.find_all('article', class_='prd _fb col c-prd')
        for product in products:
            img_c_div = product.find('div', class_='img-c')
            img_tag = img_c_div.find('img', class_='img') if img_c_div else None
            name_tag = product.find('h3', class_='name')
            new_price_tag = product.find('div', class_='prc')
            old_price_s_prc_w_div = product.find('div', class_='s-prc-w')
            if old_price_s_prc_w_div:
                old_price_tag = old_price_s_prc_w_div.find('div', class_='old')
                discount_on_old_price_tag = old_price_s_prc_w_div.find('div', class_='bdg _dsct _sm')
            else:
                old_price_tag = None
                discount_on_old_price_tag = None
            stars_div = product.find('div',class_='stars _s')
            ratings_div = stars_div.find('div', class_='in') if stars_div else None

            if img_tag and name_tag and new_price_tag or old_price_tag or discount_on_old_price_tag or ratings_div:
                img_url = img_tag['data-src'] if img_tag else None
                name = name_tag.text
                new_price = new_price_tag.text
                old_price = old_price_tag.text if old_price_tag else None
                discount_on_old_price = discount_on_old_price_tag.text if discount_on_old_price_tag else None
                if ratings_div:
                    ratings_style =  ratings_div['style'] 
                    width_value = ratings_style.split(':')[1].replace('%','').strip()
                    ratings = f'{float(width_value)/20:.1f}'
                else:
                    ratings = '0.0'
                product_info = {
                    "img_url": img_url, 'name': name, 'new_price': new_price,'old_price': old_price,'discount': discount_on_old_price, 'ratings': ratings
                }
                products_list_info.append(product_info)

    return render(request, 'core/home.html', {'products_list_info': products_list_info})