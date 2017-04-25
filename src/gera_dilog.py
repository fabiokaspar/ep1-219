#!/usr/bin/env python
# coding: utf8

# versão do python usada: Python 2.7.6

#### Gera graficos logaritmizados no eixo y
#### uso: ./gera_dilog.py

import matplotlib as mpl 
import re
import os
mpl.use('agg') ## agg backend is used to create plot as a .png file
import matplotlib.pyplot as plt 
import statistics as stat
from matplotlib.legend_handler import HandlerLine2D
import math
from pylab import *



lista_diretorios = ["mandelbrot_seq", "mandelbrot_pth", "mandelbrot_omp"]
regioes = ['full', 'seahorse', 'elephant', 'triple_spiral']
num_medicoes = 10
num_entradas = 10
threads = [1, 2, 4, 8, 16, 32]			
entradas = ['16', '32', '64', '128', '256', '512', '1024', '2048', '4096', '8192']



for diretorio in lista_diretorios:
	lista_arquivos = os.listdir("results/"+diretorio)
	Vmedia = [ [ [] for j in range(6)] for i in regioes] 

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
		arq.close()

		media = []
		for j in range(0, num_entradas):
			## define uma amostra
			amostra = numeros[(num_medicoes * j) : (num_medicoes * (j+1))]
			amostra.sort()

			media.append(stat.mean(amostra))
			

		#capturar as medias de cada grupo de dados
		if diretorio != 'mandelbrot_seq':
			for regiao in regioes:
				tipo = re.findall(regiao, arquivo)
				if len(tipo) > 0:				
					pos = regioes.index(regiao)
					num_threads = int(re.findall(r"\d+", arquivo)[0])
					threads = [1, 2, 4, 8, 16, 32]									
					Vmedia[pos][threads.index(num_threads)].append(media)


	#gerar grafico dilog de linhas para cada regiao com diferentes num de threads
	if diretorio != 'mandelbrot_seq': 

		cor = ['blue', 'black', 'red', 'green', 'orange', 'yellow']
		for mediaRegiao in Vmedia:
			grafLog = []
			for i in cor:
				grafLog.append([])

			j = 0
			for mediaThread in mediaRegiao:
				for i in range(4):
					grafLog[j].append(0) #tamanho min da imagem eh 2^4 por isso zero p 2^0 ate 2^3	
				
				figLog = plt.figure()
				plt.ylim(0.0001,100.0)
				ax = figLog.add_subplot(1,1,1)
				ax.set_xticklabels([r'$2^0$',r'$2^2$',r'$2^4$',r'$2^6$',r'$2^8$',r'$2^{10}$',r'$2^{12}$',r'$2^{14}$'])
				ax.yaxis.grid(True)
		
				plt.xlabel('Tamanho Da Entrada', fontsize=10, color='red')
				plt.ylabel('Tempo Em Segundos', fontsize=10, color='red')
				for media in mediaThread:

					for i in media:
						grafLog[j].append(i)	
				j += 1

			icor = 0
			for graf in grafLog:
				line, = ax.plot(graf, color=cor[icor], lw=2, label=str(threads[grafLog.index(graf)])+' threads')
				plt.legend(loc='upper left')
				icor += 1				
					
			ax.set_yscale('log')
			# Salva a figura
			figLog.savefig('graphics/'+diretorio+'/'+regioes[Vmedia.index(mediaRegiao)]+'_'+'log.png')
	print ''

