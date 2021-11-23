#include <stdio.h>
#include <iostream>
#include <random>
#include <ctime>
#include <time.h>
#include <chrono>
#include <ctime> 
#include <chrono> 
using namespace std;
using namespace std::chrono; 

void tri_insertion(int tab[], int taille)
{
   int i, j;
   for (i = 1; i < taille; ++i) {
       int elem = tab[i];
       for (j = i; j > 0 && tab[j-1] > elem; j--)
           tab[j] = tab[j-1];
       tab[j] = elem;
   }
}


int main(){

    int tab[10000];
    

    auto start = high_resolution_clock::now(); 
  
    
    int i, j;

    for(i=0;i<10000;i++)
    {
        j=rand()%100;
        tab[i]=j+1;
    }

    tri_insertion(tab,10000);

    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(stop - start); 
  
    cout << duration.count() << endl; 
}