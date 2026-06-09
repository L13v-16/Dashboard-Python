const carrinhoCompras = document.getElementById("carrinho-compras");
const etiqueta = document.getElementById("etiqueta");
let carrinho = JSON.parse(localStorage.getItem("carrinho")) || [];

let atualizarIconeCarrinho = () => {
    let icone = document.getElementById("quantidadeCarrinho");
    icone.innerHTML = carrinho.map((item) => item.quantidade).reduce((acumulo, quantidade) => acumulo + quantidade, 0);
}

atualizarIconeCarrinho();

let gerarItensCarrinho = () => {
    if(carrinho.length !== 0) {
        carrinhoCompras.innerHTML = carrinho.map((item) => {
            let {id, quantidade} = item;
            let produto = produtosLoja.find((produto) => produto.id === id) || {};
            let {imagem, preço, nome } = produto;

            return`
            <div class="item-carrinho">
             <img width="100" src=${imagem} />
               <div class="detalhes">
                  <div class="titulo-preco-x"> 
                       <h4 class="titulo-preco">
                          <p>${nome}</p>
                          <p class="preco-item-carrinho">${preço}</p>
                      </h4>
                      <button onclick="removerItem(${id})">Remover Item</button>
                  </div>
                  <div class="botoes-carrinho">
                      <div class="botoes">
                         <button onclick="diminuir(${id})">Remover do Carrinho</button>
                         <div id="${id}" class="quantidade">${quantidade}</div>
                         <button onclick="aumentar(${id})">Adicionar ao Carrinho</button>
                      </div>
                  </div>
                  <h3>Total: R$ ${quantidade * preço}</h3>
              </div>
            </div>
            ;`
        }).join("");
    } else {
        carrinhoCompras.innerHTML = "";
        etiqueta.innerHTML = `
        <h2>Carrinho Vazio</h2>
        <a href="index.html">
             <button class="botao-loja">Voltar para a loja</button>
        </a>
        `;
    }
}

gerarItensCarrinho();