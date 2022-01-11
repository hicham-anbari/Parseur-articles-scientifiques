import random
from datetime import datetime
import time


nowdep = time.time()

def tri_insertion(L):
    N = len(L)
    for n in range(1,N):
        cle = L[n]
        j = n-1
        while j>=0 and L[j] > cle:
            L[j+1] = L[j] # decalage
            j = j-1
        L[j+1] = cle


liste = []
for k in range(10000):
    liste.append(random.randint(0,100))

tri_insertion(liste)

nowarr = time.time()
new1 = nowarr - nowdep
print(new1)
