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
    j = (j + b) % 256;
    absorb_nibble(b % 16);
    absorb_nibble(b / 16);
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

int main(){
  int c,o;
  unsigned char key[] = "PLEASE CHANGE THE KEY VALUE017632927114";
  unsigned char out[32];
  
  fprintf(stderr,"\n");

  for (int v = 0; v < 256; v++) 
      s[v] = v;
  c = 0;
  while ( key[c++] ){
    absorb_byte(key[c]);
  }
  while ( (c = fgetc(stdin)) != -1 ){
    update();
    o = c ^ s[j];
    /* encrypt      
    absorb_byte(o);
    ****************/
    /* decrypt */     
    absorb_byte(c);
    /*****************/
    fputc((unsigned char)o, stdout);
  }
  squeeze(out, 32);
  for (int ii=0; ii<32; ii++)  
     fprintf(stderr,"%x", out[ii]);
  fprintf(stderr, "\n");
}
