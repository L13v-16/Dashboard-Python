let loja = document.getElementById("loja");
let carrinho = JSON.parse(localStorage.getItem("carrinho")) || [];

let gerarLoja = () => {
    loja.innerHTML= produtosLoja.map((produto) => {
        let { id, nome, preço, imagem } = produto;
        let itemCarrinho = carrinho.find((item) => item.id === id) || [];

        return `
        <div id="produto-${id}" class="item">
            <img width="200" src="${imagem}" />
            <div class="detalhes">
              <h3>${nome}</h3>
              <div class="preco-quantidade">
                  <h2>${preço}</h2>
                  <div class=botoes>
                    <button onclick="aumentar(${id})" class="add-to-cart">Adicionar ao Carrinho</button>
                    <div id="${id}" class="quantidade">
                        ${itemCarrinho.quantidade === undefined ? 0 : itemCarrinho.quantidade}
                    </div>
                    <button onclick="diminuir(${id})" class="remove-from-cart">Remover do Carrinho</button>
                  </div>
              </div>
            </div>
        </div>
        `;
    }).join(""); 
}

gerarLoja();

let aumentar = (id) => {
    let itemNoCarrinho = carrinho.find((item) => item.id === id);

    if(!itemNoCarrinho) {
        carrinho.push({ id: id, quantidade: 1}); 
    } else {
        itemNoCarrinho.quantidade += 1;
        
    }
    
    atualizarQuantidade(id);
    localStorage.setItem("carrinho", JSON.stringify(carrinho));
}

let diminuir = (id) => {
    let itemNoCarrinho = carrinho.find((item) => item.id === id);

    if(!itemNoCarrinho || itemNoCarrinho.quantidade === 0) return;
    itemNoCarrinho.quantidade -= 1;

    atualizarQuantidade(id);

    carrinho = carrinho.filter((item) => item.quantidade > 0);
    
    localStorage.setItem("carrinho", JSON.stringify(carrinho));
}

let atualizarQuantidade = (id) => {
    let itemAtualizado = carrinho.find((item) => item.id === id);
    document.getElementById(id).innerHTML = itemAtualizado.quantidade;

    atualizarIconeCarrinho();
}

let atualizarIconeCarrinho = (id) => {
    let icone = document.getElementById("quantidadeCarrinho");
    icone.innerHTML = carrinho.map((item) => item.quantidade).reduce((acumulo, quantidade) => acumulo + quantidade, 0);
}

atualizarIconeCarrinho();