#!/usr/bin/env python
# coding: utf8

# Referencia de como fazer boxplot: 
# http://blog.bharatbhole.com/creating-boxplots-with-matplotlib/

# versão do python usada: Python 2.7.6

from __future__ import unicode_literals

import numpy as np
import matplotlib as mpl 
import re
import os

mpl.use('agg') ## agg backend is used to create plot as a .png file
import matplotlib.pyplot as plt 

import statistics as stat

num_medicoes = 10
num_entradas = 4
lista_diretorios = ["mandelbrot_seq", "mandelbrot_pth", "mandelbrot_omp"]
regioes = ['full', 'seahorse', 'elephant', 'triple_spiral']


entradas = ['16']
rotulos = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

# calcula todos os tamanhos de entrada, mas como string
while len(entradas) < num_entradas:
	entradas.append(str(int(entradas[-1]) * 2))


###################### parser dos tempos de cada arquivo #############################
for diretorio in lista_diretorios:
	lista_arquivos = os.listdir("results/"+diretorio)

	for arquivo in lista_arquivos:
		arq = open("results/"+diretorio+"/"+arquivo, 'r')
		
		texto = arq.read() 

		tempos = re.findall(r"\d+[,.]\d+ seconds time elapsed", texto)
		numeros = []

		for x in tempos:
			aux = x.split(" seconds time elapsed")
			numeros.append(float(aux[0].replace(",", "."))) 

		# debug
		print diretorio+"/"+arquivo
		print len(numeros)
		print numeros
		arq.close()

		#################### gera o grafico ##########################

		data_to_plot = []
		media = []
		mediana = []
		dp = []

		for j in range(0, num_entradas):
			## define uma amostra
			amostra = numeros[(num_medicoes * j) : (num_medicoes * (j+1))]
			amostra.sort()

			media.append(stat.mean(amostra))
			mediana.append(stat.median(amostra))
			dp.append(stat.stdev(amostra))

			##  E a adiciona numa coleção global delas  
			data_to_plot.append(amostra)

		
		# Cria uma instancia de figura e eixos
		fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 9))

		# Cria o boxplot
		box_plot = ax.boxplot(data_to_plot)


		col_labels = ['média', 'mediana', 'desvio padrão', '< valor obs.', '> valor obs.']
		row_labels = []
		table_vals = []
		maximo = 0

		for j in range(num_entradas):
			table_vals.append([ media[j], mediana[j], dp[j], data_to_plot[j][0], data_to_plot[j][-1] ])
			row_labels.append('entr. '+ entradas[j])

			if data_to_plot[j][-1] > maximo:
				maximo = data_to_plot[j][-1]

		the_table = plt.table(cellText=table_vals,
                  colWidths = [0.1] * 5,
                  rowLabels=row_labels,
                  colLabels=col_labels,
                  bbox=[0.1, 1.2, 0.8, 0.3],
                  fontsize=24)

		the_table.scale(1.8, 1.8)
		
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

		maximo = round(maximo, 5) 
		interval = round(maximo/30.0, 5)
		print "maximo = ", maximo
		print "interval = ", interval
		print "*************************"
		
		plt.yticks(np.arange(0, maximo + interval, interval))
		
		# Salva a figura
		fig.savefig('graphics/'+diretorio+'/'+arquivo[0:-4]+'.png', bbox_inches='tight')

	print ''
