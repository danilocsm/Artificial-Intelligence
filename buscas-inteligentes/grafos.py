from collections import deque
from array import array

rede_amigos = {}

rede_amigos['eu'] = ['alice','bob','claire']
rede_amigos['bob'] = ['anuj','peggy']
rede_amigos['alice'] = ['peggy']
rede_amigos['claire'] = ['thom','jonny']
rede_amigos['anuj'] = []
rede_amigos['peggy'] = []
rede_amigos['thom'] = []
rede_amigos['jonny'] = []


caminhos = {}

caminhos[1] = [2,3]
caminhos[2] = [4,6]
caminhos[3] = [4,5]
caminhos[4] = []
caminhos[5] = [6]
caminhos[6] = []

dist = [0]*(len(caminhos.keys())+1)

dist = array('l',dist)


def pessoa_e_vendedor(nome):

	return nome[-1] == 'm'


def is_fim(state,destino):

	return state == destino

#Esta busca apenas retorna se existe um caminho de um vertice A até um vertice B
#ou se existe "algo" pré definido a se encontrar a partir de um vertice A.
'''
def busca_em_largura2(estado,destino,caminhos):

	global dist

	fathers = [-1]*(len(caminhos.keys())+1)
	fathers = array('l',fathers)


	verificados = dict(zip(caminhos.keys(),[False]*len(caminhos.keys())))

	for key in caminhos.keys():
		dist[key] = -1

	fila_de_pesquisa = deque()
	fila_de_pesquisa += caminhos[estado]

	fathers[estado] = estado


	while fila_de_pesquisa:

		actual = fila_de_pesquisa.popleft()
		if verificados[actual] == False:
			if is_fim(actual,destino):
				if fathers[actual] == -1:
					fathers[actual] = last
				print("Caminho Encontrado {0} --> {1}".format(estado,actual))
				return True
			else:
				fila_de_pesquisa += caminhos[actual]
				verificados[actual] = True

	print("Caminho Não Encontrado {0} --> {1}".format(estado,destino))
	return False
'''

def busca_em_largura1(nome,rede_amigos):

	verificadas = dict(zip(rede_amigos.keys(),[False]*8)) 
	# estrutura para verificar se uma pessoa ja foi verificada, evitando entrar em loop infinito
	
	fila_de_pesquisa = deque()
	fila_de_pesquisa += rede_amigos[nome]

	while fila_de_pesquisa:

		pessoa = fila_de_pesquisa.popleft()

		if verificadas[pessoa] == False:
			if pessoa_e_vendedor(pessoa):
				print(pessoa + " é um vendedor de manga")
				return True
			else:
				fila_de_pesquisa += rede_amigos[pessoa]
				verificadas[pessoa] = True

	return False
 

#busca_em_largura1(nome,rede_amigos)
busca_em_largura2(3,6,caminhos)