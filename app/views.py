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

        old_price_span = soup.find('span', class_='a-price a-text-price')

        if old_price_span is not None:
            # get old price of product
            old_price_text = old_price_span.get_text(strip=True)
            numeric_part = re.search(r'\$?(\d+\.\d+)', old_price_text)

            if numeric_part:
                numeric_value = float(numeric_part.group(1))
                old_price = float(numeric_value)

                # difference Price
                diff_price = price - old_price

            else:
                print("Could not extract numeric part from old price span")
        else:
            old_price = price
            diff_price = 0
            print(f"No old price found. Using current price: {old_price}")
        # Save the details into the Links model
        link = Links.objects.create(name=name,
                                    url=url,
                                    current_price=price,
                                    old_price=old_price,
                                    price_difference=diff_price)

        return redirect('index')
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid request method'
        })


def delete_url(request, id):
    if request.method == 'POST':
        link = Links.objects.get(id=id)
        link.delete()
        return redirect('index')
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid request method'
        })


def update_url(request):
    if request.method == 'POST':
        links = Links.objects.all()

        for link in links:
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
                    "Accept-Language": "en",
                }
                r = requests.get(link.url, headers=headers)
                soup = BeautifulSoup(r.text, "lxml")

                # Update name of product
                name = soup.select_one(selector="#productTitle").getText()
                name = name.strip()
                link.name = name

                # Update price of product
                whole_part = soup.select_one('.a-price-whole').get_text()
                fraction_part = soup.select_one('.a-price-fraction').get_text()
                price_str = whole_part.replace(',', '') + fraction_part
                price = float(price_str)
                link.current_price = price

                old_price_span = soup.find('span', class_='a-price a-text-price')

                if old_price_span is not None:
                    # Update old price of product
                    old_price_text = old_price_span.get_text(strip=True)
                    numeric_part = re.search(r'\$?(\d+\.\d+)', old_price_text)

                    if numeric_part:
                        numeric_value = float(numeric_part.group(1))
                        old_price = float(numeric_value)
                        link.old_price = old_price

                        # Update difference Price
                        link.price_difference = price - old_price

                    else:
                        print("Could not extract numeric part from old price span")
                else:
                    link.old_price = price
                    link.price_difference = 0
                    print(f"No old price found. Using current price: {price}")

                link.save()
            except Exception as e:
                print(f"Error updating URL: {link.url}. Error: {str(e)}")

        return redirect('index')
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
