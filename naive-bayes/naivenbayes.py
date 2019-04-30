from sklearn.naive_bayes import GaussianNB
import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import accuracy_score
from sklearn.utils import shuffle
import os

#feats = ['Idade','Altura','Tecnica','Passe','Chute','Forca','Velocidade','Drible']

def avaliaçao(cnf_matrix):

    vp = cnf_matrix[0][0] # VP
    fn = cnf_matrix[0][1] # FN
    fp = cnf_matrix[1][0] # FP
    vn = cnf_matrix[1][1] # VN

    acuracia = (vp+vn)/(vp+vn+fp+fn) # perc de acertos total
    sensibilidade = vp/(vp+fn) # perc de positivos acertados # recall
    especificidade = vn/(vn+fp) # perc de negativos acertados
    precisao = vp/(vp+fp) # prob de repetir a acuracia


    print ("acuracia = ", acuracia)
    print ("sensibilidade = ", sensibilidade)
    print ("especificidade = ", especificidade)
    print ("precisao = ", precisao)

    #return acuracia, sensibilidade



def cross_validation(dataSet,labels):

	model = GaussianNB()

	model.fit(x,y)

	resultados = cross_val_predict(model, dataSet, labels, cv=15)
	result = accuracy_score(y,resultados)
	return result

def normal_validation(dataSet,labels):

	fraction=[110,100,90,80,70]

	results = []

	model = GaussianNB()

	for fract in fraction:

		treino = dataSet[:fract]
		teste = dataSet[fract:]
		treino_labels = labels[:fract]
		teste_labels = labels[fract:]

		model.fit(treino,treino_labels)

		predicted = model.predict(teste)

		results.append(accuracy_score(teste_labels,predicted))

	results = np.asarray(results)
	soma = results.sum()

	soma = soma/5

	print(soma)


	#print(len(dataSet))
	#print(len(dataSet[:30]))


def classify(model,data):

	predicted = model.predict(data)

	return predicted

feats = ['Altura','Tecnica','Passe','Chute','Forca','Velocidade','Drible']
dataset = pd.read_csv("C:/Users/danil/Documents/trab3IA/treino.csv")
print(dataset.head())
#lassificar = pd.read_csv("C:/Users/danil/Documents/trab3IA/nao_classificados.csv")

dataset = shuffle(dataset)
print(dataset.head())
x = dataset[feats].values
y = dataset['Classe'].values


def create_model(x,y):

	model = GaussianNB()

	model.fit(x,y)

	return model

def main():

	path = "C:/Users/danil/Documents/trab3IA/nao_classificados.csv"
	feats = ['Idade','Altura','Tecnica','Passe','Chute','Forca','Velocidade','Drible']

	dataset1 = pd.read_csv("C:/Users/danil/Documents/trab3IA/treino.csv")

	dataset2 = pd.read_csv(path)
	print(dataset1['Altura'].mean())
	print(dataset1['Altura'].var())
	'''
	x, y =dataset1[feats].values, dataset1['Classe'].values

	model = create_model(x,y)

	dataset2['Classe'] = classify(model,dataset2[feats].values)

	dataset2.to_csv("C:/Users/danil/Documents/trab3IA/classificados2.csv")
	'''
if __name__ == "__main__":
	main()

#print(cross_validation(x,y))
#print(normal_validation(x,y))
#print(model.score(x,y))
