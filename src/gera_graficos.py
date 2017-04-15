#!/usr/bin/env python

# Referencia de como fazer boxplot: 
# http://blog.bharatbhole.com/creating-boxplots-with-matplotlib/

#import numpy as np
import matplotlib as mpl 
import re
import os

mpl.use('agg') ## agg backend is used to create plot as a .png file
import matplotlib.pyplot as plt 



#id_fig = 0
num_medicoes = 10
num_entradas = 5
lista_diretorios = ["mandelbrot_seq", "mandelbrot_pth", "mandelbrot_omp"]
regioes = ['full', 'seahorse', 'elephant', 'triple_spiral']


entradas = ['16']

# calcula todos os tamanhos de entrada, mas como string
while len(entradas) < num_entradas:
	entradas.append(str(int(entradas[-1]) * 2))


###################### parser dos valores do arquivo #############################
for diretorio in lista_diretorios:
	lista_arquivos = os.listdir("results/"+diretorio)

	for arquivo in lista_arquivos:
		arq = open("results/"+diretorio+"/"+arquivo, 'r')
		
		texto = arq.read() 

		tempos = re.findall(r"0,\d+ seconds time elapsed", texto)
		numeros = []

		for x in tempos:
			aux = x.split(" seconds time elapsed")
			numeros.append(float(aux[0].replace(",", "."))) 

		# debug
		print diretorio+"/"+arquivo
		print numeros
		print len(numeros)
		print type(numeros)

		print "**************\n"

		arq.close()

		#################### gera o grafico ##########################

		#numeros = np.asarray(numeros)
		#print numeros
			
		data_to_plot = []

		for j in range(num_entradas):
			## Cria uma colecao
			box_plot = numeros[num_medicoes * j : num_medicoes * (j+1)]
			
			##  E a adiciona numa lista  
			data_to_plot.append(box_plot)
			


		# Cria uma instancia de figura
		#fig = plt.figure(id_fig)
		#id_fig = id_fig+1

		# Cria uma instancia de eixos
		#ax = fig.add_subplot(111)


		fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(9, 9))

		# Cria o boxplot
		#boxplot = ax.boxplot(data_to_plot, patch_artist=True)
		boxplot = ax.boxplot(data_to_plot)

		#for patch in boxplot['boxes']:
		#	patch.set_facecolor('lightgreen')

		ax.set_xticklabels(entradas)
		ax.yaxis.grid(True)
		
		plt.xlabel('Tamanho Da Entrada', fontsize=10, color='red')
		plt.ylabel('Tempo Em Segundos', fontsize=10, color='red')


		title = './'+diretorio
		title += ', regiao: '

		for regiao in regioes:
			lista = re.findall(regiao, arquivo)			
			
			if len(lista) > 0:
				title += regiao

		
		if diretorio == 'mandelbrot_seq':
			s = arquivo[-7:-4]
			title += (', '+s.upper()+' I/O e aloc. memoria')
		
		else:
			lista = re.findall(r"\d+", arquivo)			
			title += (', #threads: '+lista[0])

		plt.title(title, fontsize=10)


		## Remove top axes and right axes ticks
		ax.get_xaxis().tick_bottom()
		ax.get_yaxis().tick_left()

		
		# Salva a figura
		fig.savefig('graphics/'+diretorio+'/'+arquivo[0:-4]+'.png', bbox_inches='tight')

