#include <stdio.h>

#define SWAP(A,B) tmp = A; A = B; B = tmp;

int a = 0, i = 0, j = 0, w = 1, s[256];
int tmp;

void update()
{
    i = (i + w) % 256;
    j = s[(j + s[i]) % 256];
    SWAP(s[i], s[j])
}

void absorb_nibble(int x)
{
    if (a == 240){ 
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
}

int output()
{
    update();
    return s[j];
}

void squeeze(char *out, size_t outlen)
{
   if (a != 0){ 
       for (int v = 0; v < 256; v++) 
           update();
       w = (w + 2) % 256;
       a = 0;
   }    
   for (int v = 0; v < outlen; v++) 
       out[v] = output();
}

int main(){
  int c;
  unsigned char out[32];
  
  printf("hash ");

  for (int v = 0; v < 256; v++) 
      s[v] = v;

  while ( (c = fgetc(stdin)) != -1 ){
    absorb_byte(c);
  }
  squeeze(out, 32);
  for (int ii=0; ii<32; ii++)  
     printf("%x", out[ii]);
  printf("\n");
}