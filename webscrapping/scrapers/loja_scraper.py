from abc import ABC, abstractmethod


class LojaScraper(ABC):

    def buscar(self, produto):
        self.abrir_site()
        self.pesquisar_produto(produto)
        self.abrir_primeiro_resultado()

        nome = self.coletar_nome()
        preco = self.coletar_preco()

        return {
            "produto_buscado": produto,
            "nome": nome,
            "preco": preco,
            "loja": self.nome_loja,
        }

    @abstractmethod
    def abrir_site(self):
        pass

    @abstractmethod
    def pesquisar_produto(self, produto):
        pass

    @abstractmethod
    def abrir_primeiro_resultado(self):
        pass

    @abstractmethod
    def coletar_nome(self):
        pass

    @abstractmethod
    def coletar_preco(self):
        pass