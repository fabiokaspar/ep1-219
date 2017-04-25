#!/usr/bin/env python

########## testa o modulo statistics.py
## uso: ./teste_stat.py

import statistics as stat


data = [0, -1, 3, 2, 4, 1, 0, 5.5, 6.777]

data.sort()

print data


media = stat.mean(data)
mediana = stat.median(data)
variancia = stat.variance(data)
dp = stat.stdev(data)

print "media = ", media
print "mediana = ", mediana
print "variancia = ", variancia
print "desvio padrao = ", dp

