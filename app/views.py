from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests
import lxml
from bs4 import BeautifulSoup
import re
from .models import Links


def index(request):
    product = Links.objects.all().order_by('-created')
    total_link = Links.objects.all().count()
    context = {
        'product': product,
        'total_link': total_link,
    }
    return render(request, 'app/index.html', context)


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
        link = Links.objects.create(name=name,
                                    url=url,
                                    current_price=price,
                                    old_price=old_price,
                                    price_difference=diff_price)
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


def delete_url(request, id):
    if request.method == 'POST':
        print(id)
        link = Links.objects.get(id=id)
        link.delete()
        return redirect('index')
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid request method'
        })
