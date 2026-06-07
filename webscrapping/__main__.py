from selenium import webdriver
from scrapers.kabum_scraper import KabumScraper

def main ():
    produtos = [
    "Havit Headphone Fone de Ouvido H2002d",
    "Mouse sem fio Logitech M170",
    "Havit Fone de Ouvido Headset Gamer Fuxi-H3",
    "Dell - KM3322W, Teclado e Mouse sem fio, Preto",
    "Mouse Sem Fio Recarregável Wireless Bluetooth Optico Led Rgb Colorido"
    ]
    navegador = webdriver.Chrome()

    kabum = KabumScraper(navegador)

    for produto in produtos:
        resultado = kabum.buscar(produto)
        print(resultado)

    navegador.quit()

if __name__ == "__main__":
    main()