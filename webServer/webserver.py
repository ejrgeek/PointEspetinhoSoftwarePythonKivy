# /bin/python3
# Coding: -*- UTF-8 -*-
# Coded By Vitor Fernandes (Rapt00r) and Erlon Jr. (ejrgeek)

import socket
import sqlite3
import sys
import pickle
import os

conexaoTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


###### CODES ######

executed = "200\n".encode() # Código de OK, executado com sucesso
error = "400\n".encode() # Código de Erro, Query Errada

####### FUNÇÕES RELACIONADAS AO SOCKET DO SERVER #######

## Criação do server
def connectionServer(ip,port):
	host = (ip,port)

	conexaoTCP.bind(host)
	conexaoTCP.listen(1)
	print("Server conectado no IP %s na porta %s" %(ip, port))

## Receber dados
def receiveData(con, client):
	print("Esperando Conexão")

	try:
		print("Conexão feita por ", cliente)
		
		while(True):
			data = con.recv(65535).decode()
			if(data):
				# Cajo haja a palavra SELECT na requisição, ele executa a query e retorna os resultados codificados
				if("SELECT" in data):

					# [:-1] retira o caractere \n da string
					resultado = selectQuery(data[:-1])
					if(resultado == []):
						continue
					else:
						resultadoEnviar = pickle.dumps(resultado) # Serializa os dados
						con.send(resultadoEnviar)

				# Cajo haja a palavra INSERT na requisição, ele executa a query e dá commit
				if("INSERT" in data):
					boole = insertQuery(data[:-1])
					if(boole):
						con.send(executed)
					else:
						con.send(error)

				# Cajo haja a palavra DELETE na requisição, ele executa a query e dá commit
				if("DELETE" in data):
					boole = deleteQuery(data[:-1])
					if(boole):
						con.send(executed)
					else:
						con.send(error)

				# Cajo haja a palavra UPDATE na requisição, ele executa a query e dá commit
				if("UPDATE" in data):
					boole = updateQuery(data[:-1])
					if(boole):
						con.send(executed)
					else:
						con.send(error)

				# Cajo haja a palavra SAIRJA na requisição, ele encerra a conexão com o cliente
				if("SAIRJA" in data):
					print("Fechando a conexão com o Cliente ", cliente)
					con.send(executed)
					con.close()
					sys.exit(0)

	finally:
		con.close()

########################################################

####### FUNÇÕES RELACIONADAS AO BANCO DE DADOS SQLITE3 #######

# Criaçao / Conexão do DB
def connectionDB(name):
	global conexaoDB
	# Abre a conexão com o banco de dados
	conexaoDB = sqlite3.connect(name)
	
# Criador do Cursor
def createCursor():
	global cursorDB
	# Define o cursor que tem como função alterar e trabalhar com o banco de dados
	cursorDB = conexaoDB.cursor() 

# Criar tabela
def createTable():
	cursorDB.execute("""
		CREATE TABLE IF NOT EXISTS pessoa (
			ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
			Nome TEXT NOT NULL,
			Idade INTEGER);
			""")
	print("Tabela pessoa criada com sucesso\n")

# Inserir dados
def insertQuery(query):
	try:
		cursorDB.execute(query)
		conexaoDB.commit()
	
	except:
		return False # Caso a query esteja errada
	return True 

# Selecionar dados
def selectQuery(query):
	try:
		cursorDB.execute(query)
	except:
		print()
	return cursorDB.fetchall() # Retorna os dados selecionados

# Deletar dados
def deleteQuery(query):
	try:
		cursorDB.execute(query)
		conexaoDB.commit()

	except:
		return False # Caso a query esteja errada
	return True 

def updateQuery(query):
	try:
		cursorDB.execute(query)
		conexaoDB.commit()
	
	except:
		return False # Caso a query esteja errada
	return True 

###############################################################

# Cria um novo server na porta passada
connectionServer('0.0.0.0', 3307)
# Se conecta com o Banco de Dados
connectionDB('nome.db')
createCursor()
createTable()
insertQuery('INSERT INTO pessoa (Nome, Idade) VALUES("Teste", 0)')

# O servidor sempre fica recebendo dados
while(True):
	con, cliente = conexaoTCP.accept()
	pid = os.fork() # Cria um novo fork para cada conexão
	if(pid == 0):
		conexaoTCP.close()
		receiveData(con, cliente)
	else:
		con.close()
