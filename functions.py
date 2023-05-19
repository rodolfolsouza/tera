import streamlit as st
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(filename='log_geral.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

load_dotenv('.env')
dbhost = os.getenv('DBHOST')
dbname = os.getenv('DBNAME')
dbuser = os.getenv('DBUSER')
dbpass = os.getenv('DBPASS')



def connect_db():
    try:
        con = mysql.connector.connect(host=dbhost,database=dbname,user=dbuser,password=dbpass)
        if con.is_connected():
            # logging.info('Conectado ao banco de dados')
            return con
    except Error as e:
        logging.error(f'Erro ao conectar ao banco de dados: {e}')

def consuta_produto(name):
    try:
        con = connect_db()
        cursor = con.cursor()
        cursor.execute(f"SELECT * FROM CADITE WHERE name like '%{name}%'")
        result = cursor.fetchall()
        return result
    except Error as e:
        logging.error(f'Erro ao consultar o banco de dados: {e}')
        return 'ERROR'
    finally:
        cursor.close()
        con.close()

def lista_de_nomes_produto():
    try:
        con = connect_db()
        cursor = con.cursor()
        cursor.execute("SELECT name,price,categoria,id FROM CADITE")
        result = cursor.fetchall()
        return result
    except Error as e:
        logging.error(f'Erro ao consultar o banco de dados: {e}')
        return 'ERROR'
    finally:
        cursor.close()
        con.close()

def gerar_recomendacao_de_produtos(categorias):
    try:
        con = connect_db()
        cursor = con.cursor()
        # if categories in the list is igual, it will be removed
        categorias = list(categorias)
        for i in categorias:
            if categorias.count(i) > 1:
                categorias.remove(i)
        print(categorias)

        # categorias = ','.join(categorias)
        # print(categorias)
        
        # cursor.execute(f"SELECT con FROM MODCAT WHERE ant like '%{categorias}%' ORDER BY lift DESC")
        # Caso tenha mais de uma categoria, tentar buscar no db usando ambas as categorias
        if len(categorias) > 1:
            cursor.execute(f"SELECT con FROM MODCAT WHERE ant like '%{categorias[0]}%' AND ant like '%{categorias[1]}%' ORDER BY lift DESC")
        else:
            cursor.execute(f"SELECT con FROM MODCAT WHERE ant like '%{categorias[0]}%' ORDER BY lift DESC")
        result = cursor.fetchall()
        # unir as tuplas em uma lista
        # separar por virgula
        result = [i[0].split(',') for i in result]
        # remover "'" e " " da lista
        result = [[j.replace("'",'') for j in i] for i in result]
        result = [i for j in result for i in j]
        # remover duplicatas
        result = list(set(result))
        print(result)
        # se a lista tiver mais de 5 itens, remover os itens excedentes
        if len(result) > 5:
            result = result[:5]
        # consultar o banco de dados e retornar os produtos
        result = tuple(result)
        produtos = []
        print(result)
        for a in result:
            print(a)
            cursor.execute(f"SELECT name,price,categoria,id FROM CADITE WHERE categoria like '%{a}%' ORDER BY RAND() LIMIT 5")
            dados = cursor.fetchall()
            for i in dados:
                produtos.append(i)
        return produtos
            

    except Error as e:
        logging.error(f'Erro ao consultar o banco de dados: {e}')
        return 'ERROR'

