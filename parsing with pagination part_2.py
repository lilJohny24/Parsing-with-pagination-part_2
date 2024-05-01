import requests
from bs4 import BeautifulSoup
base_url = 'https://parsinger.ru/html/index{}_page_{}.html'
base = 'https://parsinger.ru/html/'
full_list = []
def get_links(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            sale_buttons = soup.find_all(class_='sale_button')
            href_values = []
            for link in sale_buttons:
                href = link.find('a')['href']
                href_values.append(base + href)
            return href_values
    except Exception as e:
        print(f"Error: {e}")

all_urls = []
list_price = []
list_stock = []

def get_price_stock(a_links):
    try:
        new_response = requests.get(a_links)
        if new_response.status_code == 200:
            new_soup = BeautifulSoup(new_response.content, 'html.parser')
            price = new_soup.find('span', id = 'price')
            if price:
                new_price = int(price.get_text()[:-4])
                list_price.append(new_price)
            stock = new_soup.find('span', id = 'in_stock')
            if stock:
                new_stock = int(stock.get_text()[11:])
                list_stock.append(new_stock)
    except Exception as x:
        print(f"Error: {x}")         

for page in range(1, 5):
    for index in range(1, 6):
        url = base_url.format(index, page)
        all_urls.extend(get_links(url))
for i in all_urls:
    a_links = str(i)
    get_price_stock(a_links)

result = [x * y for x, y in zip(list_price, list_stock)]
print(sum(result))


