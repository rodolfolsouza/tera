import streamlit as st
import functions as f
import pandas as pd
import logging

logging.basicConfig(filename='log_geral.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

#open css
with open('style.css') as ww:
    st.markdown(f'<style>{ww.read()}</style>', unsafe_allow_html=True)
    
st.title("Carrinho de Compras")
# Montar carrinho de compras
lista_produtos = f.lista_de_nomes_produto()
nomes = [i[0] for i in lista_produtos]
option = st.multiselect('Selecione uma opção', nomes)
if st.button('Adicionar ao carrinho'):
    st.success(f'Foram adicionados {len(option)} produtos ao carrinho')
    produtos = []
    precos = []
    categorias = []
    ids = []
    for i in option:
        for j in lista_produtos:
            if i == j[0]:
                produtos.append(j)
                precos.append(j[1])
                categorias.append(j[2])
                ids.append(j[3])
    df = pd.DataFrame(produtos, columns=['Produto','Preço','Categoria','ID'])
    df['ID'] = ids
    df['Preço'] = precos
    # adicionar R$ to price
    df['Preço'] = df['Preço'].apply(lambda x: f'R$ {x}')
    df['Categoria'] = categorias
    # id as a string and index
    df['ID'] = df['ID'].astype(str)
    df.set_index('ID', inplace=True)
    st.dataframe(df)
    st.write(f'Total do carrinho: R$ {round(sum(precos),2)}')


    # Recomendação de produtos
    st.title("Recomendação de Produtos")
    st.write('Baseado nos produtos que você adicionou ao carrinho, recomendamos os seguintes produtos:')
    print(tuple(categorias))
    recomendacao = f.gerar_recomendacao_de_produtos(tuple(categorias))
    df = pd.DataFrame(recomendacao, columns=['Nome','Preço','Categoria','ID'])
    # adicionar R$ to price
    df['Preço'] = df['Preço'].apply(lambda x: f'R$ {x}')
    # id as a string and index
    df['ID'] = df['ID'].astype(str)
    df.set_index('ID', inplace=True)
    st.dataframe(df)


        

