/* 5b388e18e5d83714e6a9545963380273e334e363  i3.c */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>


int S[256];
unsigned int i, j, k, w, iv = 15;

void printState(){
  int ii;
  fprintf(stderr, "i %4d \n",i);
  fprintf(stderr, "j %4d \n",j);
  fprintf(stderr, "k %4d \n",k);
  fprintf(stderr, "w %4d \n",w);
  fprintf(stderr, "S-Box\n");
  for (ii = 0; ii < 256; ii++){
    fprintf(stderr, "%4d",S[ii]);
    if (ii % 16 == 15) fprintf(stderr,"\n");
  }
} 
/* KSA modified */
void rc4_init(unsigned char *key, int key_length) {
    for (i = 0; i < 256; i++)
        S[i] =  i;

     j = key_length;
     for (i = 0; i < 256; i++) {
        int tmp;
        j = (j + key[i % key_length] + S[i]) & 255;
	tmp = S[i]; S[i] = S[j]; S[j] = tmp;
     }
	     
     i = S[0]; 
     j = S[1]; 
     k = S[2]; 
     w = (2*S[4] + 1) % 256;
     printState();
}
 
int main(int narg, char **argv) {
   int cin, tmp;
   int cnt = 0;
   rc4_init((unsigned char *)argv[1], strlen(argv[1]));
   printState();
    while(!feof(stdin)){
       int out, rnd;
       j = j + iv;
       i = (i + w) & 255;
       j = (k + S[(j + S[i]) & 255]) & 255;
       k = (i + k + S[j]) & 255;		 
       tmp = S[i]; S[i] = S[j]; S[j] = tmp;    
       rnd = S[(j + k) & 255];
       cin = fgetc(stdin);
       out = (unsigned char)cin ^ rnd;
       iv = out; 
       if ( cin != -1 ) {
           fputc(out, stdout);
	    cnt++;
       }
       if (cnt == 1) printState();	   
    }	   
}
