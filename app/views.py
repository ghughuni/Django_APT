from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests
import lxml
from bs4 import BeautifulSoup
import re
from .models import Links
from .serializers import LinksSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response



def index(request):
    product = Links.objects.all().order_by('-date')
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
        
        # r = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")
        
        # get img_url of product
        img_tag = soup.select_one("#landingImage")
        if img_tag:
            img_url = img_tag.get('src')
            # print("Image URL:", img_url)
        else:
            print("No img tag found inside the div with id 'imgTagWrapperId'")


        # get name of product
        name_element = soup.select_one(selector="#productTitle")
        if name_element:
            name = name_element.getText().strip()
            # print("Product Name:", name)
        else:
            print(f"No product title found for URL: {url}")
            # Handle the case where the product title is not found
            return JsonResponse({'status': 'error', 'message': 'Product title not found'})

        # get price of product
        whole_part = soup.select_one('.a-price-whole')
        fraction_part = soup.select_one('.a-price-fraction')
        if whole_part and fraction_part:
            whole_part_text = whole_part.get_text()
            fraction_part_text = fraction_part.get_text()
            price_str = whole_part_text.replace(',', '') + fraction_part_text
            price = float(price_str)
        else:
            print(f"No price elements found for URL: {url}")
            # Handle the case where the price elements are not found
            return JsonResponse({'status': 'error', 'message': 'Price elements not found'})

        old_price_span = soup.find('span', class_='a-price a-text-price')

        if old_price_span:
            # get old price of product
            old_price_text = old_price_span.get_text(strip=True)
            numeric_part = re.search(r'\$?(\d+\.\d+)', old_price_text)

            if numeric_part:
                numeric_value = float(numeric_part.group(1))
                old_price = float(numeric_value)

                # difference Price
                diff_price = price - old_price
                diff_price = round(diff_price, 2)

            else:
                print("Could not extract numeric part from old price span")
                # Handle the case where the numeric part is not found in the old price span
                return JsonResponse({'status': 'error', 'message': 'Numeric part not found in old price span'})
        else:
            old_price = price
            diff_price = 0
            print(f"No old price found. Using current price: {old_price}")

        # Save the details into the Links model
        link = Links.objects.create(name=name,
                                    url=url,
                                    img_url=img_url,
                                    current_price=price,
                                    old_price=old_price,
                                    price_difference=diff_price)

        return redirect('index')
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

# Delete Product
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

# Updates of Product Data
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
                # r = requests.get(link.url)
                soup = BeautifulSoup(r.text, "lxml")

                # Update name of product
                name_element = soup.select_one(selector="#productTitle")
                if name_element is not None:
                    name = name_element.getText()
                    name = name.strip()
                    link.name = name
                else:
                    print(f"Could not find product title for URL: {link.url}")


                # Update price of product
                whole_part = soup.select_one('.a-price-whole')
                fraction_part = soup.select_one('.a-price-fraction')
                if whole_part is not None and fraction_part is not None:
                    whole_part_text = whole_part.get_text()
                    fraction_part_text = fraction_part.get_text()
                    price_str = whole_part_text.replace(',', '') + fraction_part_text
                    price = float(price_str)
                    link.current_price = price
                else:
                    print(f"Could not find price elements for URL: {link.url}")
                    
                    
                # Update old price of product
                old_price_span = soup.find('span', class_='a-price a-text-price')
                if old_price_span is not None:
                    old_price_text = old_price_span.get_text(strip=True)
                    numeric_part = re.search(r'\$?(\d+\.\d+)', old_price_text)

                    if numeric_part:
                        numeric_value = float(numeric_part.group(1))
                        old_price = float(numeric_value)
                        link.old_price = old_price

                        # Update difference Price
                        link.price_difference = price - old_price
                        link.price_difference = round(link.price_difference, 2)
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



###################
### API Section ###
###################

# List all products
@api_view(['GET'])
def links_list(request):
    if request.method == 'GET':
        links = Links.objects.all()
        serializer = LinksSerializer(links, many=True)
        return Response(serializer.data)

# Product Details
@api_view(['GET'])
def link_details(request, pk):
    try:
        link = Links.objects.get(id=pk)
        serializer = LinksSerializer(link)
        return Response(serializer.data)
    except Links.DoesNotExist:
        return JsonResponse({'message': 'Invalid ID, NOT FOUND'})
    
        
        
