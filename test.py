from datetime import datetime
import time

nowdep = time.time()

fichier = open('Das_Martins1.txt', 'r')
i=0

for ligne in fichier:
	print(ligne)
	i = i+1

fichier.close()

nowarr = time.time()
print(" i = ",i)

print "time au debut =", nowdep

print "time a la fin =", nowarr

new1 = nowarr - nowdep
print "temps d'execution : ", new1
