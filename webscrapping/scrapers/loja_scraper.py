from abc import ABC, abstractmethod


class LojaScraper(ABC):

    def buscar(self, produto):
        self.abrir_site()
        self.pesquisar_produto(produto)
        self.abrir_primeiro_resultado()

        nome = self.coletar_nome()
        preco = self.coletar_preco()

        return f"{nome} -> {preco}"

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