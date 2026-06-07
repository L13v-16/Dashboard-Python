import json
import re
from pathlib import Path

import pandas as pd

DADOS_DIR = Path(__file__).resolve().parent.parent / "dados"
ARQUIVO_BRUTO = DADOS_DIR / "produtos_brutos.csv"
ARQUIVO_LIMPO = DADOS_DIR / "produtos_limpos.csv"
ARQUIVO_JSON = DADOS_DIR / "produtos.json"

COLUNAS_TEXTO = ["produto_buscado", "nome", "preco", "loja"]
PRECO_NAO_ENCONTRADO = "Preço não encontrado"


def carregar_dados(caminho=None):
    arquivo = Path(caminho) if caminho else ARQUIVO_BRUTO

    if not arquivo.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {arquivo}\n"
            "Execute o webscraping antes: python -m webscrapping"
        )

    return pd.read_csv(arquivo, encoding="utf-8")


def converter_preco_brasileiro(preco):
    if pd.isna(preco):
        return None

    texto = str(preco).strip()
    if not texto or texto == PRECO_NAO_ENCONTRADO:
        return None

    numeros = re.sub(r"[^\d,.]", "", texto)
    if not numeros:
        return None

    if "," in numeros:
        numeros = numeros.replace(".", "").replace(",", ".")

    try:
        return float(numeros)
    except ValueError:
        return None


def limpar_texto(valor):
    if pd.isna(valor):
        return None
    return re.sub(r"\s+", " ", str(valor).strip())


def limpar_dados(df):
    dados = df.copy()
    dados.columns = dados.columns.str.strip().str.lower()

    for coluna in COLUNAS_TEXTO:
        if coluna in dados.columns:
            dados[coluna] = dados[coluna].apply(limpar_texto)

    if "data_coleta" in dados.columns:
        dados["data_coleta"] = pd.to_datetime(
            dados["data_coleta"], errors="coerce"
        )

    dados["preco_numerico"] = dados["preco"].apply(converter_preco_brasileiro)
    dados["preco_disponivel"] = dados["preco_numerico"].notna()
    dados["preco_formatado"] = dados["preco_numerico"].apply(
        lambda valor: f"R$ {valor:,.2f}".replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
        if pd.notna(valor)
        else PRECO_NAO_ENCONTRADO
    )

    dados = dados.drop_duplicates(
        subset=["produto_buscado", "loja", "nome"],
        keep="last",
    )

    dados = dados.sort_values(
        by=["loja", "produto_buscado"],
        na_position="last",
    ).reset_index(drop=True)

    return dados


def salvar_dados_limpos(df, caminho=None):
    arquivo = Path(caminho) if caminho else ARQUIVO_LIMPO
    arquivo.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(arquivo, index=False, encoding="utf-8")
    return arquivo


def exportar_json(df, caminho=None):
    arquivo = Path(caminho) if caminho else ARQUIVO_JSON
    arquivo.parent.mkdir(parents=True, exist_ok=True)

    registros = []
    for _, linha in df.iterrows():
        data_coleta = linha.get("data_coleta")
        if pd.notna(data_coleta):
            data_coleta = pd.Timestamp(data_coleta).isoformat()
        else:
            data_coleta = None

        preco_numerico = linha.get("preco_numerico")
        if pd.isna(preco_numerico):
            preco_numerico = None
        else:
            preco_numerico = round(float(preco_numerico), 2)

        registros.append({
            "produto_buscado": linha["produto_buscado"],
            "nome": linha["nome"],
            "preco_original": linha["preco"],
            "preco_numerico": preco_numerico,
            "preco_formatado": linha["preco_formatado"],
            "preco_disponivel": bool(linha["preco_disponivel"]),
            "loja": linha["loja"],
            "data_coleta": data_coleta,
        })

    with arquivo.open("w", encoding="utf-8") as saida:
        json.dump(registros, saida, ensure_ascii=False, indent=2)

    return arquivo


def exibir_resumo(df):
    print("\n=== Resumo dos dados limpos ===")
    print(f"Total de produtos: {len(df)}")
    print(f"Com preço válido: {df['preco_disponivel'].sum()}")
    print(f"Sem preço: {(~df['preco_disponivel']).sum()}")

    if df["preco_disponivel"].any():
        print(f"Preço mínimo: R$ {df['preco_numerico'].min():,.2f}")
        print(f"Preço máximo: R$ {df['preco_numerico'].max():,.2f}")
        print(f"Preço médio: R$ {df['preco_numerico'].mean():,.2f}")

    print("\n=== Tabela limpa ===")
    colunas_exibir = [
        "produto_buscado",
        "nome",
        "preco_formatado",
        "loja",
        "preco_disponivel",
    ]
    print(df[colunas_exibir].to_string(index=False))


def processar_nova_coleta(caminho=None):
    brutos = carregar_dados(caminho)
    limpos = limpar_dados(brutos)
    arquivo_csv = salvar_dados_limpos(limpos)
    arquivo_json = exportar_json(limpos)

    print(f"\n[Pandas] Coleta processada: {len(brutos)} registros")
    print(f"[Pandas] CSV limpo: {arquivo_csv}")
    print(f"[Pandas] JSON para o banco: {arquivo_json}")

    return limpos


def main():
    limpos = processar_nova_coleta()
    exibir_resumo(limpos)
    return limpos


if __name__ == "__main__":
    main()
