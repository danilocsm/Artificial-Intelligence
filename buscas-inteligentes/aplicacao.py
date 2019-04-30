from collections import deque

# estrutura que guarda as distancias heuristicas

min_dist = {'aracaju':[('fortaleza',815),('jpessoa',486),('salvador',277)]
				,'fortaleza':[('jpessoa',555),('salvador',1028)],
				'jpessoa':[('fortaleza',555),('salvador',763)],
				'maceio':[('fortaleza',730),('jpessoa',299),('salvador',475)],
				'natal':[('fortaleza',435),('jpessoa',151),('salvador',875)],
				'recife':[('fortaleza',629),('jpessoa',104),('salvador',675)],
				'salvador':[('fortaleza',1028),('jpessoa',763)],
				'saoluis':[('fortaleza',652),('jpessoa',1162),('salvador',1323)],
				'teresina':[('fortaleza',495),('jpessoa',905),('salvador',994)]}


# constroí um grafo contendo as cidades do nordeste, as adjacencias e seus respectivos pesos para cada vertice.

def create_Graph():

	graph = {}

	graph['aracaju'] = [('maceio',294),('salvador',356)]
	graph['fortaleza'] = [('natal',537),('recife',800),('teresina',634)]
	graph['jpessoa'] = [('natal',185),('recife',120)]
	graph['maceio'] = [('aracaju',294),('recife',285)]
	graph['natal'] = [('fortaleza',537),('jpessoa',185)]
	graph['recife'] = [('fortaleza',800),('jpessoa',120),('maceio',285),('teresina',1137)]
	graph['salvador'] = [('aracaju',356),('teresina',1163)]
	graph['saoluis'] = [('teresina',446)]
	graph['teresina'] = [('fortaleza',634),('recife',1137),('salvador',1163),('saoluis',446)]

	return graph


# função que verifica se o objetivo foi atingido
def is_destiny(city,objective):

	#print("Cidade 1 {0}  Cidade 2 {1}".format(city,objective))
	if city == objective:
		return True
	else:
		return False

# algoritmo da busca em profundidade em um grafo
# utilizado para realizar a busca em profundidade para achar um possivel resultado

def my_DFS(origin,objective,graph):

	father = {}
	# estrutura para guardar o pai de cada n
	for key in graph.keys():
		father[key] = None

	verified = dict(zip(graph.keys(),[False]*9))
	# estrutura para verificar se uma cidade ja foi verificada, evitando entrar em loop infinito

	filo = []
	filo += [origin]
	last = []
	# estrutura para controlar a escolha de apenas um caminho, resultando em apenas um pai
	while filo:

		thisCity = filo.pop(-1)

		for item in graph[thisCity]:

			if verified[thisCity] == False:
				if item[0] not in last:
					father[item[0]] = thisCity
				if item[0] not in filo:
					filo += [item[0]]

		last.insert(0,thisCity)
		verified[thisCity] = True
		if thisCity == objective:
			break

	return father


# algoritmo da busca em largura em um grafo
# utilizado para realizar a busca em extensão para achar um possivel resultado
def my_BFS(origin,objective,graph):

	father = {}
	# estrutura para guardar o pai de cada nó

	for key in graph.keys():

		father[key] = None

	#print(father)

	verified = dict(zip(graph.keys(),[False]*9))
	# estrutura para verificar se uma cidade ja foi verificada, evitando entrar em loop infinito

	fifo = deque()
	fifo += [origin]
	last = [] # estrutura para controlar a escolha de apenas um caminho, resultando em apenas um pai

	while fifo:

		thisCity = fifo.popleft()

		#print(thisCity)
		for item in graph[thisCity]:
			#print(item)
			if verified[thisCity] == False:
				if(item[0] not in last):
					father[item[0]] = thisCity
				if item[0] not in fifo:
					fifo += [item[0]]

		last.insert(0,thisCity)
		verified[thisCity] = True
		if thisCity == objective:
			break

	#print(verified)
	return father


def ava_function(cost,origin,destiny):

	global min_dist

	heuristic = 0

	for item in min_dist[origin]:
		if item[0] == destiny:
			heuristic = item[1]

	return cost+heuristic



#busca A* utilizando a heuristica da distancia em linha reta de um ponto até o destino
def search_A_star(origin,destiny,graph):

	child = {}

	for key in graph.keys():
		child[key] = None

	verified = dict(zip(graph.keys(),[False]*9))
	# estrutura para verificar se uma cidade ja foi verificada, evitando entrar em loop infinito

	name_fifo = [] #verifica os nomes que já estao na fila
	ord_list = [] #fila ordenada em forma crescente com segundo a função de avaliação
	ord_list += [(origin,ava_function(0,origin,destiny))]
	name_fifo += [origin]

	while ord_list:

		next_city = ord_list.pop(0)

		for item in graph[next_city[0]]:

			if verified[next_city[0]] == False:
				if item[0] not in name_fifo:
					ord_list += [(item[0],ava_function(item[1],item[0],destiny))]
					name_fifo += [ item[0]]


		verified[next_city[0]] == True
		ord_list.sort(key = lambda x:x[1])
		child[next_city[0]] = ord_list[0][0]

		if next_city[0] == destiny:
			break

	return child

#função que cria o caminho da origem até o objetivo, não necessariamente é o caminho ótimo
def create_path1(origin,destiny,father,sequence):

	if is_destiny(origin,destiny):
		sequence.append(origin)
	else:
		if father[destiny] == None:
			print("No Path found")
		else:
			create_path1(origin,father[destiny],father,sequence)
			sequence.append(destiny)


#função que cria o caminho da origem até o objetivo usando a busca A*
def create_path2(origin,destiny,child,sequence):

	nextt = origin
	while nextt!= destiny:

		sequence.append(nextt)
		nextt = child[nextt]

	sequence.append(nextt)

def agent_function_BFS(origin,destiny,graph):

	action_seq = []
	initial_state = origin

	if not action_seq:

		aux = my_DFS(origin,destiny,graph) #aux recebe os pais
		create_path1(origin,destiny,aux,action_seq)

	return action_seq


#função do agente busca cega por extensão
def agent_function_A_star(origin,destiny,graph):

	action_seq = []
	initial_state = origin

	if not action_seq:

		aux = search_A_star(origin,destiny,graph) #aux recebe os filhos
		create_path2(origin,destiny,aux,action_seq)

	return action_seq

def show_path(seq):

	while seq:
		print("{0} ---> ".format(seq.pop(0)),end = "")

	print("end")

def main():

	#print(min_dist)

	sequence = []
	nordeste = create_Graph()

	#BUSCA CEGA POR EXTENSAO
	print("______________________________________________________________________")
	print("**Trajeto de São Luís até João Pessoa utilizando busca cega por extensão")
	print("")
	sequence = (agent_function_BFS('saoluis','jpessoa',nordeste))
	show_path(sequence)


	print("______________________________________________________________________")
	print("**Trajeto de Fortaleza até Salvador utilizando busca cega por extensão")
	print("")
	sequence = (agent_function_BFS('fortaleza','salvador',nordeste))
	show_path(sequence)

	print("______________________________________________________________________")
	print("**Trajeto de Salvador até Fortaleza utilizando busca cega por extensão")
	print("")
	sequence = (agent_function_BFS('salvador','fortaleza',nordeste))
	show_path(sequence)


	print("______________________________________________________________________")
	print("**Trajeto de João Pessoa até São Luís utilizando busca cega por extensão")
	print("")
	sequence = (agent_function_BFS('jpessoa','saoluis',nordeste))
	show_path(sequence)



	#BUSCA COM INFORMAÇÃO A*
	print("______________________________________________________________________")
	print("**Trajeto de São Luís até João Pessoa utilizando busca com informação A*")
	print("")
	sequence = (agent_function_A_star('saoluis','jpessoa',nordeste))
	aux = sequence[::-1]
	show_path(sequence)

	print("______________________________________________________________________")
	print("**Trajeto de Fortaleza até Salvador utilizando busca com informação A*")
	print("")
	sequence = (agent_function_A_star('fortaleza','salvador',nordeste))
	show_path(sequence)

	print("______________________________________________________________________")
	print("**Trajeto de Salvador até Fortaleza utilizando busca com informação A*")
	print("")
	sequence = (agent_function_A_star('salvador','fortaleza',nordeste))
	show_path(sequence)

	print("______________________________________________________________________")
	print("**Trajeto de João Pessoa até São Luís utilizando busca com informação A*")
	print("")
	sequence = aux # jpessoa sao luis busca estrela
	show_path(sequence)


if __name__ == "__main__":
	main()
