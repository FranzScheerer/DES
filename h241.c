#include <stdio.h>
#include <stdlib.h>

#define SWAP(A,B) tmp = A; A = B; B = tmp;

int a = 0, i = 0, j = 0, w = 1, s[256];
int tmp;

void update()
{
    i = (i + w) % 256;
    j = s[(j + s[i]) % 256];
    SWAP(s[i], s[j])
}
int output()
{
    update();
    return s[j];
}

void absorb_nibble(int x)
{
    if (a == 241){ 
       for (int v = 0; v < 256; v++) 
           update();
       w = (w + 2) % 256;
       a = 0;
    }
    SWAP(s[a], s[x+240])
    a++;
}

void absorb_byte(int b)
{
    absorb_nibble(b % 16);
    absorb_nibble(b / 16);
    j = (j + b) % 256;
}


void squeeze(char *out, size_t outlen)
{
   int v;
   for (v = 0; v < 256; v++) 
       update();
   w = (w + 2) % 256;
   a = 0;
   for (v = 0; v < outlen; v++) 
       out[v] = output();
}

int main(int argn, char *argv[]){
  int c,ii;
  char txt[] = "The quick brown fox jumps over the lazy dog";
  FILE *fp;
  unsigned char out[32];
  
  fprintf(stderr,"hash %s\n",txt);
  a = i = j = 0;
  w = 1;
  for (int v = 0; v < 256; v++) 
     s[v] = v;
  c = 0;
  while ( txt[c] ){
     absorb_byte(txt[c++]);
  }
  squeeze(out, 32);
  for (int ii=0; ii<32; ii++)  
     fprintf(stderr,"%x", out[ii]);
  fprintf(stderr, "\n");
  a = i = j = 0;
  w = 1;
  for (int v = 0; v < 256; v++) 
     s[v] = v;
  c = 0;

  if (argn == 1){
    fprintf(stderr,"Usage ./a.out <filename>\n" );
    fprintf(stderr,"Read from stdin ...\n" );
    while ( (c = fgetc(stdin)) != -1 ){
        absorb_byte(c);
    }
  } else {
    fp = fopen(argv[1],"rb");
    if (!fp){
      fprintf(stderr,"error reading file %s\n",argv[1] );
      exit(0);
    }
    while ( (c = fgetc(fp)) != -1 ){
        absorb_byte(c);
    }
    fclose(fp);
  }
  squeeze(out, 32);
  for (int ii=0; ii<32; ii++)  
     fprintf(stderr,"%x", out[ii]);
  fprintf(stderr, "\n");
}
