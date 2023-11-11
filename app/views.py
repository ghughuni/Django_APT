from django.shortcuts import render
from django.http import JsonResponse
import requests
import lxml
from bs4 import BeautifulSoup

# exampls:
# url = 'https://www.amazon.com/DELL-Inspiron-15-3525-Business/dp/B0CKSBRSHL/ref=sr_1_1_sspa?crid=K8L8H6L6CK7S&keywords=dell%2Bvostro%2B5630%2Blaptop&qid=1699697758&sprefix=dell%2Bvostro%2Blaptop%2B5%2Caps%2C205&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1'
# url = 'https://www.amazon.com/PlayStation-5-Console-CFI-1215A01X/dp/B0BCNKKZ91/ref=sr_1_1?crid=2ZIOKC4AP9XG4&keywords=playstation%2B5%2Bconsole&psr=EY17&qid=1699700486&s=todays-deals&sprefix=playstation%2B5%2Ctodays-deals%2C208&sr=1-1&th=1'
# url = 'https://www.amazon.com/Apple-iPhone-12-Pro-Max/dp/B09JFFG8D7/ref=sr_1_2?crid=3UAHPBW9A4XUW&keywords=iphone%2B15&qid=1699700647&refinements=p_89%3AApple&rnid=2528832011&s=wireless&sprefix=iphone%2B15%2Caps%2C251&sr=1-2&th=1'
def index(request):
    url = 'https://www.amazon.com/Apple-iPhone-12-Pro-Max/dp/B09JFFG8D7/ref=sr_1_2?crid=3UAHPBW9A4XUW&keywords=iphone%2B15&qid=1699700647&refinements=p_89%3AApple&rnid=2528832011&s=wireless&sprefix=iphone%2B15%2Caps%2C251&sr=1-2&th=1'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
        "Accept-Language": "en",

    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")

    # get name of product
    name = soup.select_one(selector="#productTitle").getText()
    name = name.strip()

    # get price of product
    price = soup.select_one(selector=".a-price-whole").getText()
    fraction = soup.select_one(selector=".a-price-fraction").getText()
    price = float(price + fraction)


    context = {
        'name': name,
        'price': price,

    }


    return render(request, 'app/index.html', context)
