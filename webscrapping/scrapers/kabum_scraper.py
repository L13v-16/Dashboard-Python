from .loja_scraper import LojaScraper
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class KabumScraper(LojaScraper):

    def __init__(self, navegador):
        self.navegador = navegador
        self.url = "https://www.kabum.com.br/"

    def abrir_site(self):
        self.navegador.get(self.url)

    def pesquisar_produto(self, produto):
        barra_busca = WebDriverWait(self.navegador, 10).until(
            EC.element_to_be_clickable((By.ID, "inputBusca"))
        )

        barra_busca.clear()
        barra_busca.click()
        barra_busca.send_keys(produto)
        barra_busca.send_keys(Keys.ENTER)

    def abrir_primeiro_resultado(self):
        primeiro_produto = WebDriverWait(self.navegador, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '(//a[contains(@href, "/produto/")])[1]')
            )
        )

        primeiro_produto.click()

    def coletar_nome(self):
        nome = WebDriverWait(self.navegador, 10).until(
            EC.visibility_of_element_located((By.TAG_NAME, "h1"))
        )

        return nome.text

    def coletar_preco(self):
        try:
            preco = WebDriverWait(self.navegador, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//h4[contains(text(),"R$")]')
                )
            )

            return preco.text

        except:
            return "Preço não encontrado"