import streamlit as st
import functions as f
import pandas as pd

st.title("Pesquisa de Produtos Disponiveis")

# sidebar icon menu on top
# Pesquisar produtos disponiveis
search = st.text_input('Pesquisar')
if st.button('Pesquisar'):
    result = f.consuta_produto(search)
    # loading
    with st.spinner('Carregando...'):
        if result == 'ERROR':
            st.error(f'Não foi possivel localizar produtos com o nome {search}')
        else:
            st.success(f'Foram localizados {len(result)} produtos com o nome {search.capitalize()}')
            df = pd.DataFrame(result, columns=['ID','Nome','Preço','Categoria','Subcategoria'])
            # Id as a string and index
            df['ID'] = df['ID'].astype(str)
            # R$ to price
            df['Preço'] = df['Preço'].apply(lambda x: f'R$ {x}')
            df.set_index('ID', inplace=True)
            st.divider()
            st.dataframe(df)

# loading style.css
with open('style.css') as ww:
    st.markdown(f'<style>{ww.read()}</style>', unsafe_allow_html=True)