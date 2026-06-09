from bs4 import BeautifulSoup
import requests

url = "https://www.amazon.com.br/Bleach-Box-Set-Volumes-1-21/dp/1421526107"

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

title = soup.find("span", id="productTitle")
symbol = soup.find("span", class_="a-price-symbol")
whole = soup.find("span", class_="a-price-whole")
fraction = soup.find("span", class_="a-price-fraction")

if symbol and whole and fraction:
    price = f"{title.get_text()} -> {symbol.get_text()}{whole.get_text()}{fraction.get_text()}"
    print(price)
else:
    print("Preço não encontrado.")