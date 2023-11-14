from django.shortcuts import render
from django.http import JsonResponse
import requests
import lxml
from bs4 import BeautifulSoup
import re
from .models import Links


def index(request):
    product = Links.objects.all()
    return render(request, 'app/index.html', {'product': product})


def add_url(request):
    if request.method == 'POST':
        url = request.POST.get('url', '')
        headers = {
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
            "Accept-Language": "en",
        }
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "lxml")

        # get name of product
        name = soup.select_one(selector="#productTitle").getText()
        name = name.strip()

        # get price of product
        whole_part = soup.select_one('.a-price-whole').get_text()
        fraction_part = soup.select_one('.a-price-fraction').get_text()
        price_str = whole_part.replace(',', '') + fraction_part
        price = float(price_str)

        try:
            # get old price of product
            old_price_span = soup.find('span', class_='a-price a-text-price')
            old_price_text = old_price_span.get_text()
            numeric_part = re.search(r'\d+,\d+\.\d+', old_price_text).group()
            numeric_part = numeric_part.replace(',', '')
            old_price = float(numeric_part)

            # difference Price
            diff_price = price - old_price
        except:
            old_price = price
            diff_price = 0

        # Save the details into the Links model
        link = Links.objects.create(name=name, url=url, current_price=price, old_price=old_price, price_difference=diff_price)
        context = {
            'name': name,
            'price': price,
            'url': url,
            'old_price': old_price,
            'diff_price': diff_price,
        }

        return render(request, 'app/index.html', context)
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid request method'
        })

# def index(request):
#     url = 'https://www.amazon.com/ASUS-ROG-Strix-Gaming-Laptop/dp/B0CFW1LK57/?_encoding=UTF8&ref_=dlx_deals_sc_dcl_img_dt_dealz_vi&pd_rd_w=EnBrQ&content-id=amzn1.sym.c301c913-f534-4fe9-a512-2f6d8f0fc88b&pf_rd_p=c301c913-f534-4fe9-a512-2f6d8f0fc88b&pf_rd_r=F5Q0BBVNBJYQM9WKMQ6W&pd_rd_wg=HZlev&pd_rd_r=949f5eb2-43c9-4e58-a909-dff1b2a84a83&th=1'
#     headers = {
#         "User-Agent":
#         "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
#         "Accept-Language": "en",
#     }
#     r = requests.get(url, headers=headers)
#     soup = BeautifulSoup(r.text, "lxml")

#     # get name of product
#     name = soup.select_one(selector="#productTitle").getText()
#     name = name.strip()

#     # get price of product
#     whole_part = soup.select_one('.a-price-whole').get_text()
#     fraction_part = soup.select_one('.a-price-fraction').get_text()
#     price_str = whole_part.replace(',', '') + fraction_part
#     price = float(price_str)

#     try:
#         # get old price of product
#         old_price_span = soup.find('span', class_='a-price a-text-price')
#         old_price_text = old_price_span.get_text()
#         numeric_part = re.search(r'\d+,\d+\.\d+', old_price_text).group()
#         numeric_part = numeric_part.replace(',', '')
#         old_price = float(numeric_part)

#         # difference Price
#         diff_price = price - old_price
#     except:
#         old_price = price
#         diff_price = 0

#     context = {
#         'name': name,
#         'price': price,
#         'url': url,
#         'old_price': old_price,
#         'diff_price': diff_price,
#     }

#     return render(request, 'app/index.html', context)
