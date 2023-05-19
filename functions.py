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
            logging.info('Conectado ao banco de dados')
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
        cursor.execute(f"SELECT con FROM MODCAT WHERE ant in {categorias}")
        result = cursor.fetchall()
        return result
    except Error as e:
        logging.error(f'Erro ao consultar o banco de dados: {e}')
        return 'ERROR'

