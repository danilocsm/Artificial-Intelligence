# Reversi
import random
import sys
from reversi_aux import Node,Root

#best_moves = [[0,0],[7,0],[0,7],[7,7],[2,0],[5,0],[2,2],[7,5],[5,2],[0,2],[0,5],[7,5],[5,5],[5,7],[2,7],[2,5]]

'''
PositionValues = [
    [120, -20, 20,  5,  5, 20, -20, 120],
    [-20, -40, -5, -5, -5, -5, -40, -20],
    [ 20,  -5, 15,  3,  3, 15,  -5,  20],
    [  5,  -5,  3,  3,  3,  3,  -5,   5],
    [  5,  -5,  3,  3,  3,  3,  -5,   5],
    [ 20,  -5, 15,  3,  3, 15,  -5,  20],
    [-20, -40, -5, -5, -5, -5, -40, -20],
    [120, -20, 20,  5,  5, 20, -20, 120],
]

'''
_root = Root(Node(None,None))
playerTile = ''
computerTile = ''
	

def drawBoard(board):
	# Essa funcao desenha o tabuleiro
	HLINE = '  +---+---+---+---+---+---+---+---+'
	VLINE = '  |   |   |   |   |   |   |   |   |'

	print('    1   2   3   4   5   6   7   8')
	print(HLINE)

	for y in range(8):
		print(VLINE)
		print(y+1, end=' ')
		for x in range(8):
			print('| %s' % (board[x][y]), end=' ')
		print('|')
		print(VLINE)
		print(HLINE)

def resetBoard(board):
	#Essa funcao esvazia o tabuleiro
	for x in range(8):
		for y in range(8):
			board[x][y] = ' '
	# Pecas iniciais:
	board[3][3] = 'X'
	board[3][4] = 'O'
	board[4][3] = 'O'
	board[4][4] = 'X'

def getNewBoard():
	# Criar um tabuleiro novo
	board = []
	for i in range(8):
		board.append([' '] * 8)
	return board

def isValidMove(board, tile, xstart, ystart):
	# Retorna False se o movimento em xstart, ystart é invalido
	# Se o movimento é valido, retorna uma lista de casas que devem ser viradas após o movimento
	if board[xstart][ystart] != ' ' or not isOnBoard(xstart, ystart):
		return False
	board[xstart][ystart] = tile 
	if tile == 'X':
		otherTile = 'O'
	else:
		otherTile = 'X'
	tilesToFlip = []
	for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
		x, y = xstart, ystart
		x += xdirection # first step in the direction
		y += ydirection # first step in the direction
		if isOnBoard(x, y) and board[x][y] == otherTile:
			x += xdirection
			y += ydirection
			if not isOnBoard(x, y):
				continue
			while board[x][y] == otherTile:
				x += xdirection
				y += ydirection
				if not isOnBoard(x, y):
					break
			if not isOnBoard(x, y):
				continue
			if board[x][y] == tile:
				while True:
					x -= xdirection
					y -= ydirection
					if x == xstart and y == ystart:
						break
					tilesToFlip.append([x, y])
	board[xstart][ystart] = ' '
	if len(tilesToFlip) == 0:
		return False
	return tilesToFlip
 
def isOnBoard(x, y):
	# Retorna True se a casa está no tabuleiro.
	return x >= 0 and x <= 7 and y >= 0 and y <=7

def getBoardWithValidMoves(board, tile):
	# Retorna um tabuleiro com os movimentos validos
	dupeBoard = getBoardCopy(board)
	for x, y in getValidMoves(dupeBoard, tile):
		dupeBoard[x][y] = '.'
	return dupeBoard

def getValidMoves(board, tile):
	# Retorna uma lista de movimentos validos
	validMoves = []
	for x in range(8):
		for y in range(8):
			if isValidMove(board, tile, x, y) != False:
				validMoves.append([x, y])
	return validMoves

# HEURISTICA FRACA. Utiliza apenas a qnt de pontos por jogadas sem avaliar nenhuma outra situação
def getScoreOfBoard(board):
	# Determina o score baseado na contagem de 'X' e 'O'.
	xscore = 0
	oscore = 0
	for x in range(8):
		for y in range(8):
			if board[x][y] == 'X':
				xscore += 1
			if board[x][y] == 'O':
				oscore += 1
	return {'X':xscore, 'O':oscore}

def enterPlayerTile():
	# Permite que o player escolha ser X ou O
	tile = ''
	while not (tile == 'X' or tile == 'O'):
		print('Escolha suas peças: X ou O?')
		tile = input().upper()
	if tile == 'X':
		return ['X', 'O']
	else:
	  return ['O', 'X']

def whoGoesFirst():
	# Escolhe aleatóriamente quem começa.
	if random.randint(0, 1) == 0:
		return 'computer'
	else:
		return 'player'

def playAgain():
	# Retorna True se o player quer jogar novamente
	print('Quer jogar novamente? (yes ou no)')
	return input().lower().startswith('y')

def makeMove(board, tile, xstart, ystart):
	# Coloca a peça no tabuleiro em xstart, ystart, e as peças do oponente
	# Retorna False se for um movimento invalido
	tilesToFlip = isValidMove(board, tile, xstart, ystart)
	if tilesToFlip == False:
		return False
	board[xstart][ystart] = tile
	for x, y in tilesToFlip:
		board[x][y] = tile
	return True

def getBoardCopy(board):
	# Faz uma cópia do tabuleiro e retorna a cópia
	dupeBoard = getNewBoard()
	for x in range(8):
		for y in range(8):
			dupeBoard[x][y] = board[x][y]
	return dupeBoard

def isOnCorner(x, y):
	# Retorna True se a posição x, y é um dos cantos do tabuleiro
	return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)

def getPlayerMove(board, playerTile):
	# Permite que o player insira sua jogada
	DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()
	while True:
		print('Insira seu movimento, ou insira quit para sair do jogo, ou hints para ativar/desativar dicas.')
		move = input().lower()
		if move == 'quit':
			return 'quit'
		if move == 'hints':
			return 'hints'
		if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
			x = int(move[0]) - 1
			y = int(move[1]) - 1
			if isValidMove(board, playerTile, x, y) == False:
			  print('Essa não é uma jogada válida')
			  continue
			else:
			  break
		else:
			print('Essa não é uma jogada válida, digite o valor de x (1-8), depois o valor de y (1-8).')
			print('Por exemplo, 81 será o canto superior direito.')
	return [x, y]

def getComputerMove(board, computerTile):
	# Permite ao computador executar seu movimento
	possibleMoves = getValidMoves(board, computerTile)
	# randomiza a ordem dos possíveis movimentos
	random.shuffle(possibleMoves)
	# se for possivel, joga no canto
	for x, y in possibleMoves:
		if isOnCorner(x, y):
			return [x, y]
	# Escolhe a jogada que resulta em mais pontos
	bestScore = -1
	for x, y in possibleMoves:
		dupeBoard = getBoardCopy(board)
		makeMove(dupeBoard, computerTile, x, y)
		score = getScoreOfBoard(dupeBoard)[computerTile]
		if score > bestScore:
			bestMove = [x, y]
			bestScore = score
	return bestMove

def showPoints(playerTile, computerTile, mainBoard):
	# Mostra o score atual
	scores = getScoreOfBoard(mainBoard)
	print('Player1: %s ponto(s). \nComputador: %s ponto(s).' % (scores[playerTile], scores[computerTile]))



#####################################################################################
# Funções que implementam o algoritmo MINMAX para busca competitiva do jogo Reversi #

# Funçao heuristica que combina diferença de peças, numero de movimentos possiveis, peças proximas aos cantos e peças
# localizadas nos cantos

def my_heuristic(board):

	global playerTile
	global computerTile
	
	# variaveis que vão guardar o valor de cada heuristica
	p,c,l,m,f,d = [0]*6

	player_tiles , computer_tiles = 0,0
	comp_front_tiles, player_front_tiles = 0,0
	
	X1 = [-1,-1,0,1,1,1,0,-1]
	Y1 = [0,1,1,1,0,-1,-1,-1]

	# tabela com a pontuação para a posição das peças
	V = [
		[20,-3,11,8,8,11,-3,20],
		[-3,-7,-4,1,1,-4,-7,-3],
		[11,-4,2,2,2,2,-4,11],
		[8,1,2,-3,-3,2,1,8],
		[8,1,2,-3,-3,2,1,8],
		[11,-4,2,2,2,2,-4,11],
		[-3,-7,-4,1,1,-4,-7,-3],
		[20,-3,11,8,8,11,-3,20]
	]

	# diferença entre as peças do player e do computador nas posições de pontuação maior
	for i in range(0,8):
		for j in range(0,8):
			if board[i][j] == computerTile:
				d += V[i][j]
				computer_tiles += 1
			elif board[i][j] == playerTile:
				d -= V[i][j]
				player_tiles += 1
			if board[i][j] != ' ':
				for k in range(0,8):
					x = i + X1[k]
					y = j + Y1[k]
					if x >=0 and x <8 and y >= 0 and y <8 and board[x][y] == ' ':
						if board[i][j] == computerTile:
							comp_front_tiles += 1
						else:
							player_front_tiles += 1
						break

	if computer_tiles > player_tiles:
		p = (100*computer_tiles)/(computer_tiles+player_tiles)
	elif computer_tiles < player_tiles:
		p = -(100*player_tiles)/(computer_tiles+player_tiles)
	else:
		 p = 0

	if comp_front_tiles > player_front_tiles:
		f = -(100*comp_front_tiles)/(comp_front_tiles+player_front_tiles)
	elif comp_front_tiles < player_front_tiles:
		f = (100*player_front_tiles)/(comp_front_tiles+player_front_tiles)
	else:
		f = 0

	# corner occupancy
	computer_tiles = 0
	player_tiles = 0

	if(board[0][0] == computerTile): 
		computer_tiles += 1
	elif(board[0][0] == playerTile):
		player_tiles += 1
	if(board[0][7] == computerTile): 
		computer_tiles += 1
	elif(board[0][7] == playerTile): 
		player_tiles += 1
	if(board[7][0] == computerTile): 
		computer_tiles += 1
	elif(board[7][0] == playerTile): 
		player_tiles += 1
	if(board[7][7] == computerTile): 
		computer_tiles += 1
	elif(board[7][7] == playerTile): 
		player_tiles += 1
	c = 25 * (computer_tiles - player_tiles)

	# corner closeness

	computer_tiles = 0
	player_tiles = 0

	if(board[0][0] == ' '):
		if(board[0][1] == computerTile):
			 computer_tiles += 1
		elif(board[0][1] == playerTile):
			 player_tiles += 1
		if(board[1][1] == computerTile):
			 computer_tiles += 1
		elif(board[1][1] == playerTile):
			 player_tiles += 1
		if(board[1][0] == computerTile):
			 computer_tiles += 1
		elif(board[1][0] == playerTile):
			 player_tiles += 1
	
	if(board[0][7] == ' '):
		if(board[0][6] == computerTile):
			 computer_tiles += 1
		elif(board[0][6] == playerTile):
			 player_tiles += 1
		if(board[1][6] == computerTile):
			 computer_tiles += 1
		elif(board[1][6] == playerTile):
			 player_tiles += 1
		if(board[1][7] == computerTile):
			 computer_tiles += 1
		elif(board[1][7] == playerTile):
			 player_tiles += 1
	
	if(board[7][0] == ' '):
		if(board[7][1] == computerTile):
			 computer_tiles += 1
		elif(board[7][1] == playerTile):
			 player_tiles += 1
		if(board[6][1] == computerTile):
			 computer_tiles += 1
		elif(board[6][1] == playerTile):
			 player_tiles += 1
		if(board[6][0] == computerTile):
			 computer_tiles += 1
		elif(board[6][0] == playerTile):
			 player_tiles += 1
	
	if(board[7][7] == ' '):
		if(board[6][7] == computerTile):
			 computer_tiles += 1
		elif(board[6][7] == playerTile):
			 player_tiles += 1
		if(board[6][6] == computerTile):
			 computer_tiles += 1
		elif(board[6][6] == playerTile):
			 player_tiles += 1
		if(board[7][6] == computerTile):
			 computer_tiles += 1
		elif(board[7][6] == playerTile):
			 player_tiles += 1
	
	l = -12.5 * (computer_tiles - player_tiles)

	# Mobility
	compMoves = len(getValidMoves(board,computerTile))
	playerMoves = len(getValidMoves(board,playerTile))

	if compMoves > playerMoves:
		m = (100*compMoves)/(compMoves+playerMoves)
	elif compMoves < playerMoves:
		m = -(100*playerMoves)/(compMoves + playerMoves)
	else:
		m = 0

	score = (10*p) + (801.724*c) + (382.026*l) + (78.922*m) + (74.396*f) + (10*d)

	return score

best_node = None

def my_max(root,depth):

	global best_node
	auxMove = None

	# verificia se chegou em uma folha ou atingiu a profundidade maxima
	if root.childs == None or depth == 0:

		return root.data[1]

	v = None	
		
	# laço para retornar o maior valor entre os filhos na camada 
	for child in root.childs:
		#print("v = {0}".format(v))
		#print(child.data)
		auxV = my_min(child,depth-1)
		#print("auxV = {0}".format(auxV))
		if v == None:
			v = auxV
			auxMove = child.data[2]
		elif auxV > v:
			v = auxV
			auxMove = child.data[2]

	best_node = auxMove

	return v

def my_min(root,depth):

	global best_node
	auxMove = None
	#print("DEPTH = {}".format(depth))
	# verificia se chegou em uma folha ou atingiu a profundidade maxima
	if root.childs == None or depth == 0:

		return root.data[1]


	v = None
	# laço para retornar o menor valor entre os filhos na camada 
	for child in root.childs:
		#print("v = {0}".format(v))

		#print(child.data)
		auxV = my_max(child,depth-1)
		#print("auxV = {0}".format(auxV))
		if v == None:
			v = auxV
			auxMove = child.data[2]
		elif auxV < v:
			v = auxV
			auxMove = child.data[2]
			

	best_node = auxMove

	return v

# funçao auxiliar que executa o algoritmo MINMAX
def minmax(root):

	global best_node
	my_max(root,5)

	return best_node

# funçao que irá, em conjunto com a funçao constroyAllMoves, construir a árvore
# de todas as jogadas possiveis até uma profundidade pré-determinada
def initializeTree(root,board):

	global computerTile
	# inicializa a raiz com o estado atual do tabuleiro
	dupeBoard = getBoardCopy(board)
	root.data = (dupeBoard,0)

	# constroi a partir da raiz estabelecida todas as possiveis jogadas até uma profundidade 5
	constroyAllMoves(root,board,computerTile,5)

def constroyAllMoves(root,board,tile,max_depth):

	global playerTile
	global computerTile
	global PositionValues

	initialMoves = getValidMoves(board, tile)
		
	aux = root
	# verifica se existem movimentos
	if initialMoves != []:
		# gera todos os possiveis estados sucessores para o nó em questão
		while initialMoves:

			#print("TURNO DO {0}".format(tile))
			#print("PROFUNDIDADE {0}".format(max_depth))
			dupeBoard = getBoardCopy(board)
			x,y = initialMoves.pop(0)
			makeMove(dupeBoard,tile,x,y)
			score = my_heuristic(dupeBoard)
			#drawBoard(dupeBoard)
			aux.insert_childs((dupeBoard,score,[x,y]))
		max_depth -= 1		
		#verifica se ainda é possivel descer na arvore
		if max_depth>0:	
			# escolhe quem gerará os tabuleiros do próximo nivel
			if max_depth % 2 == 1:
				turn_tile =  computerTile
			else:
				turn_tile = playerTile
			# gera os filhos dos filhos até a profundidade máxima ser atingida
			for i in range(0,len(root.childs)):
				constroyAllMoves(root.childs[i],root.childs[i].data[0],turn_tile,max_depth)

# funçao que apenas retornar o movimento da rodada		
def getComputerMoveMINMAX(root,board):
	
	'''
	global computerTile
	possibleMoves = getValidMoves(board,computerTile)
	for x, y in possibleMoves:
		if [x,y] in best_moves:
			return [x,y]	
	'''
	move = minmax(root)
	return move
#####################################################################################################

def start_game():
	print('Welcome to Reversi!')
	
	global playerTile
	global computerTile
	global _root
	global best_moves

	while True:
		# Reseta o jogo e o tabuleiro
		mainBoard = getNewBoard()
		resetBoard(mainBoard)
		playerTile, computerTile = enterPlayerTile()
		showHints = False
		turn = whoGoesFirst()
		print('O ' + turn + ' começa o jogo.')
		#_root.root.walk_on_tree()
		#print(moves_graph)
		
		while True:
			if turn == 'player':
				# Player's turn.
				if showHints:
					validMovesBoard = getBoardWithValidMoves(mainBoard, playerTile)
					drawBoard(validMovesBoard)
				else:
					drawBoard(mainBoard)
				showPoints(playerTile, computerTile,mainBoard)
				move = getPlayerMove(mainBoard, playerTile)
				if move == 'quit':
					print('Obrigado por jogar!')
					sys.exit() # terminate the program
				elif move == 'hints':
					showHints = not showHints
					continue
				else:
					makeMove(mainBoard, playerTile, move[0], move[1])
				if getValidMoves(mainBoard, computerTile) == []:
					break
				else:
					turn = 'computer'
			else:
				# Computer's turn.
				drawBoard(mainBoard)
				showPoints(playerTile, computerTile,mainBoard)
				input('Pressione Enter para ver a jogada do computador.')
		
			 	
				initializeTree(_root.root,mainBoard)
				x, y = getComputerMoveMINMAX(_root.root,mainBoard)
				makeMove(mainBoard, computerTile, x, y)
				_root.delete_tree()
				if getValidMoves(mainBoard, playerTile) == []:
					break
				else:
					turn = 'player'
		# Mostra o resultado final.
		drawBoard(mainBoard)
		scores = getScoreOfBoard(mainBoard)
		print('X: %s ponto(s) \nO: %s ponto(s).' % (scores['X'], scores['O']))
		if scores[playerTile] > scores[computerTile]:
			print('Você venceu o computador por %s ponto(s)! \nParabéns!' % (scores[playerTile] - scores[computerTile]))
		elif scores[playerTile] < scores[computerTile]:
			print('Você perdeu!\nO computador venceu você por %s ponto(s).' % (scores[computerTile] - scores[playerTile]))
		else:
			print('Empate!')
		if not playAgain():
			break

if __name__ == "__main__":

	start_game()