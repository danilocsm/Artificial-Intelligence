import pandas as pd
import numpy as np
import math as m
from sklearn.utils import shuffle

#              prior X likelihood
# posterior =  --------------------
#                  evidence


# prior = probabilidade de ser a classe  Ck.
# likelihood = probabilide da caracterísitica v para a classe Ck



####################################################################################
# Esta função calcula os valores da média e da variância para cada característica, #
# para serem posteriormente utilizadas para o cálculo da densidade probabilistica. #
####################################################################################
def fit(dataset):

	not_in = ["Classe","Idade","Id"] # features que não serão utilizadas
	data = []
	for col in dataset.columns:      # varre a tabela e calcula a média e a variância para cada característica
		if col not in not_in :

			data.append(dataset[col].mean())
			data.append(dataset[col].var())

	return data

#######################################################################################################################
# Esta função irá de fato criar o modelo baseado no Gaussian Naive Bayes, que se baseia pela densidade probabilistica #
# de cada características. São separados um número igual das duas classes para manter um balanço do set de treino. 	  #
#######################################################################################################################
def constroy_model(dataset):


	strikers = dataset[dataset['Classe'] == 'Atacante']
	defensors = dataset[dataset['Classe'] == 'Defensor']

	strikers = shuffle(strikers)
	defensors = shuffle(defensors)
	train_set1 = strikers	# seleciona uma quantidade da classe Atacante(30).
	train_set2 = defensors # seleciona uma quantidade da classe Defensor(30).

	data = []
	#print(len(test_set))
	data.extend(fit(train_set1)) # preenche com a média e variância de cada feat para a classe Atacante
	data.extend(fit(train_set2)) # preenche com a média e variância de cada feat para a classe Defensor

	data = np.asarray(data).reshape(2,14)

	# constroi a tabela com os dados do set de treino
	classifier = pd.DataFrame(data,index=['Atacante','Defensor'],
		columns=  [['Altura','Altura',
			'Tecnica','Tecnica',
			'Passe','Passe',
			'Chute','Chute',
			'Forca','Forca',
			'Velocidade','Velocidade',
			'Drible','Drible'],
			['mean','var',
			'mean','var',
			'mean','var',
			'mean','var',
			'mean','var',
			'mean','var',
			'mean','var']])


	return classifier

############################################################################################################################
# Esta função recebe uma classe e um vetor de valores das características e calcula a posterior para a classe em questão.  #
############################################################################################################################
def compute_posterior(model,category,feats):

	last = ''
	gnb = 1 # gaussianNaiveBayes probability distribuition value of some feat v to a given class Ck.
	i = 0
	for column in model.columns:

		if column[0] == last:
			continue
		#print(column[0])
		feat = feats[i] # vetor de valores das caracteristicas selecionadas
		#print(feat)
		mean, var = model.loc[category,column[0]]
		gnb *= gaussianNB(mean,var,feat)
		i += 1
		last = column[0]

	return gnb

#####################################################################################################
# Esta função calcula a distribuição de probabilidade de certa característica v para uma classe Ck. #
# Utiliza o método Gaussian Naive Bayes. Assume se que os dados possuem uma distribuição normal.    #
#####################################################################################################
def gaussianNB(mean,var,feat):

	pi = m.pi
	pot = -(m.pow((feat-mean),2))/(2*var)
	output = (1/(m.sqrt(2*pi*var)))*m.exp(pot)
	return output

'''
def compute_evidence(prob1,prob2,label1,label2):

	factor1 = compute_posterior(classifier,'Atacante')
	factor2 = compute_posterior(classifier,'Atacante')

'''

#########################################################################################################
# Esta função recebe o modelo treinado e um vetor de características de uma amostra a ser classificada. #
# Retorna uma dada classe baseado no funcionamento do classificador.                                    #
#########################################################################################################
def predict(classifier,feat_values):

	#evidence = compute_evidence(prob_striker,prob_defensor,'Atacante','Defensor')
	striker = compute_posterior(classifier,'Atacante',feat_values)  # calcula a posterior para a classe Atacante.
	striker = striker*(0.5) # multiplcia pelo valor de probabilidade de ser a classe atacante(50%) Prior.
	defensor = compute_posterior(classifier,'Defensor',feat_values) # calcula a posterior para a classe Defensor.
	defensor = defensor*(0.5) # multiplcia pelo valor de probabilidade de ser a classe defensor(50%) Prior.

	if striker > defensor:
		return 'Atacante'
	else:
		return 'Defensor'

###########################################################################
# Esta função classifica uma dada amostra baseado nas feats selecionadas. #
###########################################################################
def classify(model,dataset):

	feats = ['Altura','Tecnica','Passe','Chute','Forca','Velocidade','Drible'] # características selecionadas para o classificador

	#for index in dataset.index:

	feats_values = list(dataset[feats])

	labels = predict(model,feats_values)
	#print(labels)

	return labels

####################################################
# Esta função calcula a acurácia do classificador. #
####################################################
def accuracy(output, labels):

	count = 0
	total = len(labels) 										#melhorar esta funçao

	for i in range(0,total):

		if output[i] == labels[i]:
			count += 1

	print("Acuracia foi de {0}\n\n".format(count/total))

	return count/total

'''
def k_folders(data,folds):

	#data = shuffle(data)
	my_slice = 12
	k = int(len(data)/folds)
	beg = 0
	end = my_slice
	for i in range(0,k):				# MELHORAR ESTA FUNÇÃO
		folder = data.iloc[beg:my_slice]
		#print(folder.index[0])
		aux = data.copy()
		#print(list(folder.index))
		aux.drop(list(folder.index))
		model = constrol_model(aux)
		for
		beg = end
		end = end + 12
		#print(aux.iloc[0])
	pass
'''

def leave_one_out(data):

	output = []
	for i in range(0,len(data)):

		one_out = data.iloc[i]
		#print(one_out)
		aux = data.copy()
		aux.drop(i)
		model = constrol_model(aux)
		output.append(classify(model,one_out))
		#print(len(output))

	#print(output)
	print("Leave One Out")
	accuracy(output,data['Classe'].values)


def main():

	dataframe = pd.read_csv("C:/Users/danil/Documents/trab3IA/treino.csv")
	new_dataframe = pd.read_csv("C:/Users/danil/Documents/trab3IA/nao_classificados.csv")

	#output = classify(classifier,test_set)

	leave_one_out(dataframe)
	#k_folders(dataframe,10)
	'''
	accuracy(output,test_set['Classe'].values)
	new_dataframe['Classe'] = classify(classifier,new_dataframe)
	print(new_dataframe.head())
	print(new_dataframe.tail())
	new_dataframe.to_csv("C:/Users/danil/Documents/trab3IA/classificados3.csv")
	'''
	#print(test_set)


if __name__ == "__main__":

	main()
