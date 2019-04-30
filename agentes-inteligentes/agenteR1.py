


'''
O objetivo do agente A é capturar todos os * da tela no menor tempo possível.
1 - Escreva a função do agente seguindo o modelo reativo simples.
2 - Escreva a função do agente seguindo o modelo reativo baseado em objetivos.
3 - Escreva a função do agente seguindo o modelo reativo baseado em utilidade.

Depois compare o tempo que cada abordagem demorou para atingir o objetivo.

O agente capta com seus sensores o conteudo das 4 casas ao seu redor (esquerda, direita, cima, baixo)
O agente tem como acoes movimentar-se para esquerda (0), direita (1), cima (2), baixo (3)

Obs.: A função de agente implementada como exemplo representa um agente aleatório, 
qualquer abordagem que você desenvolver, deve ser no mínimo melhor que o aleatório.
'''


#Distância Euclidiana
def dist(x,y):   
    return numpy.sqrt(numpy.sum((x-y)**2))

#Bibliotecas

import numpy as np 
from random import randint
import time
import os

#Variáveis globais

SIZE = 52

posAgenteX = 1
posAgenteY = 1

remindX = 10000
remindY = 10000

flag = False

goal = {}

ambiente = np.zeros([SIZE,SIZE])

#Métodos

def delay(tempo):
	for i in range(0,tempo):
		pass

def construirAmbiente():
	
	global ambiente
	global SIZE

	for i in range(0,SIZE):
		for j in range(0,SIZE):
			if i == 0 or i == SIZE-1:
				if j == 0 or j == SIZE-1:
					ambiente[i][j] = 2
				else:
					ambiente[i][j] = 3
			elif j == 0 or j == SIZE-1:
				ambiente[i][j] = 4
			else:
				ambiente[i][j] = randint(0,1)		

def atualizarAmbiente(acao):

	global ambiente
	global posAgenteX
	global posAgenteY

	ambiente[posAgenteX][posAgenteY] = 0

	if acao == 0 and ambiente[posAgenteX][posAgenteY-1] < 2:
		posAgenteY-=1
	elif acao == 1 and ambiente[posAgenteX][posAgenteY+1] < 2 :
		posAgenteY +=1
	elif acao == 2 and ambiente[posAgenteX-1][posAgenteY] < 2 :
		posAgenteX -=1
	elif acao == 3 and ambiente[posAgenteX+1][posAgenteY] < 2 :
		posAgenteX +=1
	ambiente[posAgenteX][posAgenteY] = 5

def mostrarAmbiente():

	global ambiente
	global SIZE
	count = 0

	for i in range(0,SIZE):
		for j in range(0,SIZE):
	 		if ambiente[i][j] == 0:
	 			print(" ", end="")
	 		elif ambiente[i][j] == 1:
	 			count+=1
	 			print("*", end ="")
	 		elif ambiente[i][j] == 2:
	 			print("+", end ="")
	 		elif ambiente[i][j] == 3:
	 			print("-", end ="")
	 		elif ambiente[i][j] == 4:
	 			print("|", end ="")
	 		elif ambiente[i][j] == 5:
	 			print("A", end ="")
		print("")

	print("Faltam {0} objetos".format(count))

def verificarSucesso():

	global ambiente
	global SIZE

	for i in range(0,SIZE):
		for j in range(0,SIZE):
			if ambiente[i][j] == 1:
				return False

	return True

def lerSensor(lado):
	
	global ambiente
	global posAgenteX
	global posAgenteY

	if lado == 0:
		return ambiente[posAgenteX][posAgenteY-1]			
	if lado == 1:
		return ambiente[posAgenteX][posAgenteY+1]
	if lado == 2:
		return ambiente[posAgenteX-1][posAgenteY]
	if lado == 3:
		return ambiente[posAgenteX+1][posAgenteY]		
	 
	return 2


def tabelaDeUtilidade():

	global ambiente
	global goal

	keys = [i for i in range(1,51)]
	values = []

	for i in range(1,SIZE-1):
		array = np.where(ambiente[:][i]== 1)
		values.append(len(array[0]))

	goal = dict(zip(keys,values))


def pegaProximaUtilidade():

	key = (max(goal.keys(), key = (lambda k: goal[k])))
	goal.pop(key)

	return key

def vaiPraUtilidade(objetivo):

	global posAgenteY

	if objetivo > posAgenteY :
		while(posAgenteY != objetivo):
			posAgenteY+=1
	else:
		while(posAgenteY != objetivo):
			posAgenteY-=1


'''
Agente sempre tenta ler as 4 direçoes e limpa a primeira q ele achar um objeto. Ele se move aleatoriamente
'''
def funcaoAgenteReativoSimples(esquerda, direita, cima, baixo):
	#delay(10000)
	
	if esquerda == 1:
		return 0
	if direita == 1:
		return 1 
	if cima == 1:
		return 2
	if baixo == 1:
		return 3
	
	return randint(0,4)


'''
limpa o ambiente da direita pra esquerda, seguindo cima --> baixo,
baixo --> cima
'''
# objetivo do agente é limpar fileiras  consecutivas


def funcaoAgenteReativoBaseadoEmObjetivo(esquerda, direita, cima, baixo):

	global posAgenteX
	global posAgenteY

	#delay(10000)
	#print("x:{0} Y:{1}".format(posAgenteX,posAgenteY))

	if posAgenteY%2 == 1:

		if baixo == 3:	
			return 1
		else:
			return 3
	else:

		if cima == 3:
			return 1
		else:
			return 2

'''
O agente fica feliz qnd ele limpa uma coluna com a maior qnt de itens
'''

def funcaoAgenteReativoBaseadoEmUtilidade():

	global posAgenteX
	global posAgenteY

	if lerSensor(2) == 3 :
		while lerSensor(3) != 3:
			atualizarAmbiente(3)
	elif lerSensor(3) == 3:
		while lerSensor(2) != 3:
			atualizarAmbiente(2)


def funcaoAgente(esquerda,direita,cima,baixo):
	
	#delay(10000)
	'''
	if esquerda == 1:
		return 0
	if direita == 1:
		return 1 
	if cima == 1:
		return 2
	if baixo == 1:
		return 3
'''
	return randint(0,4)

def main():

	global posAgenteX
	global posAgenteY
	global flag
	global remindY
	global remindX

	construirAmbiente()
	mostrarAmbiente()
	tabelaDeUtilidade()
	inicio = time.time()

	while(not verificarSucesso()):

		#delay(100000000)
		utilidade = pegaProximaUtilidade()
		vaiPraUtilidade(utilidade)
		funcaoAgenteReativoBaseadoEmUtilidade()
		#acao = funcaoAgenteReativoBaseadoEmObjetivo(lerSensor(0),lerSensor(1),lerSensor(2),lerSensor(3))
		#atualizarAmbiente(acao)		
		
	fim = time.time()
	os.system("clear")
	mostrarAmbiente()
	print("Tempo de execução ----> {0}".format(fim-inicio))
	
main()
