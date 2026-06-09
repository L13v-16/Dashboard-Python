import csv
import sys
from datetime import datetime
from pathlib import Path

from selenium import webdriver

from scrapers.kabum_scraper import KabumScraper

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "tratamentodedados"))
from tratamentodedados.main_pandas import processar_nova_coleta

PRODUTOS = [
    "Havit Headphone Fone de Ouvido H2002d",
    "Mouse sem fio Logitech M170",
    "Havit Fone de Ouvido Headset Gamer Fuxi-H3",
    "Dell - KM3322W, Teclado e Mouse sem fio, Preto",
    "Mouse Sem Fio Recarregável Wireless Bluetooth Optico Led Rgb Colorido",
]

DADOS_DIR = Path(__file__).resolve().parent.parent / "dados"
ARQUIVO_BRUTO = DADOS_DIR / "produtos_brutos.csv"
COLUNAS = ["produto_buscado", "nome", "preco", "loja", "data_coleta"]


def salvar_resultados(resultados):
    DADOS_DIR.mkdir(parents=True, exist_ok=True)

    with ARQUIVO_BRUTO.open("w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=COLUNAS)
        escritor.writeheader()
        escritor.writerows(resultados)


def main():
    navegador = webdriver.Chrome()
    kabum = KabumScraper(navegador)
    data_coleta = datetime.now().isoformat(timespec="seconds")
    resultados = []

    for produto in PRODUTOS:
        resultado = kabum.buscar(produto)
        resultado["data_coleta"] = data_coleta
        resultados.append(resultado)
        print(f"{resultado['nome']} -> {resultado['preco']}")

    salvar_resultados(resultados)
    print(f"\nColeta salva em: {ARQUIVO_BRUTO}")

    processar_nova_coleta()

    navegador.quit()


if __name__ == "__main__":
    main()
