#como construir a fucking tree

#from node import Node
from random import randint

class Node:

	def __init__(self,data,childs):
		
		self.data = data
		#self.father = father
		self.childs = childs

	#def __str__():
	def create_list(self):

		if self.childs == None:
			self.childs = []
		
	def insert_childs(self,data):

		self.create_list()
		aux = Node(data,None)
		self.childs.append(aux)
		'''
	def walk_on_tree(self):
		
		if self != None:
			#print("Data: {0}\nFather: {1}\nChild Len: {2}".format(self.data,self.father,len(self.childs)))
			if self.childs != None:
				print("Data: {0}\nFather: {1}\nChild Len: {2}".format(self.data,self.father,len(self.childs)))
			
				for node in self.childs:

					node.walk_on_tree()
'''

class Root:

	def __init__(self,root):
		self.root = root


	def delete_tree(self):

		self.root.childs.clear()
		self.root.childs = None
		self.root.data = None


'''
i = 0
root = Root(Node(None,None,None))
aux = root.root

aux.insert_childs(root,4)
aux.insert_childs(root,5)
aux.insert_childs(root,6)
for node in aux.childs:
	
	node.insert_childs(node,i)
	i += 1

root.root.walk_on_tree(aux)
#print(root.possibleMoves[0])
'
aux.data = randint(0,100)

best_node = None


def my_max(root,depth):

	global best_node
	auxMove = None

	if root.childs == None or depth == 0:

		return root.data

	v = None	
		
	for child in root.childs:
		print("v = {0}".format(v))
		#print(child.data)
		auxV = my_min(child,depth-1)
		print("auxV = {0}".format(auxV))
		if v == None:
			v = auxV
			auxMove = child
		elif auxV > v:
			v = auxV
			auxMove = child

	best_node = auxMove

	return v

def my_min(root,depth):

	global best_node
	auxMove = None
	print("DEPTH = {}".format(depth))
	if root.childs == None or depth == 0:

		return root.data


	v = None
		
	for child in root.childs:
		print("v = {0}".format(v))

		#print(child.data)
		auxV = my_max(child,depth-1)
		print("auxV = {0}".format(auxV))
		if v == None:
			v = auxV
			auxMove = child
		elif auxV < v:
			v = auxV
			auxMove = child
			

	best_node = auxMove

	return v


def minmax(root):

	my_max(root,4)

	return best_node.data

def generate_numbers():

	output = []

	for i in range(0,randint(1,5)):

		output.append(randint(randint(1,10),randint(100,100)))

	return output		


h = 5
def create_tree(root):

	global h
	numbers = generate_numbers()

	while numbers:

		num = numbers.pop(0)

		root.insert_childs(root,num)

	h -= 1
	if h>0:	 
		for i in range(0,len(root.childs)):

			create_tree(root.childs[i])

create_tree(aux)

aux.walk_on_tree()
print(minmax(aux))
root.delete_tree()
#aux.walk_on_tree(aux)
'''