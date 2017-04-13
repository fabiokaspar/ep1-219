# Referencia de como fazer boxplot: 
# http://blog.bharatbhole.com/creating-boxplots-with-matplotlib/

import numpy as np
import matplotlib as mpl 
import re
import os

mpl.use('agg') ## agg backend is used to create plot as a .png file
import matplotlib.pyplot as plt 


###################### parser dos valores do arquivo #############################
num_fig = 0
lista_diretorios = ["mandelbrot_seq","mandelbrot_pth","mandelbrot_omp"]

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
		print "**************\n"

		arq.close()

	# ###################### gera o grafico #############################

		numeros = np.asarray(numeros)

		num_testes = 10

		## Create data
		box_plot_1 = numeros[num_testes*0:num_testes*1]
		box_plot_2 = numeros[num_testes*1:num_testes*2]
		box_plot_3 = numeros[num_testes*2:num_testes*3]
		box_plot_4 = numeros[num_testes*3:num_testes*4]
		box_plot_5 = numeros[num_testes*4:num_testes*5]

		## combine these different collections into a list    
		data_to_plot = [box_plot_1, box_plot_2, box_plot_3, box_plot_4, box_plot_5]

		# Create a figure instance
		fig = plt.figure(num_fig, figsize=(9, 6))

		# Create an axes instance
		ax = fig.add_subplot(111)

		# Create the boxplot
		bp = ax.boxplot(data_to_plot)

		ax.set_xticklabels(['2**4', '2**5', '2**6', '2**7', '2**8'])

		## Remove top axes and right axes ticks
		ax.get_xaxis().tick_bottom()
		ax.get_yaxis().tick_left()

		# Save the figure
		fig.savefig("img/"+diretorio+"_"+arquivo+'.png', bbox_inches='tight')

		num_fig = num_fig+1
