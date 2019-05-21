#include <stdio.h>
#include <string.h>

#define N 256
#define ROUNDS 3

int main(int argn, char **argv){
  char key[256] = "Nobody understands quantum mechanics";
  int s[N], s_[N];
  int klen,t,i,j=0;
  int i2,j2;
  int r, c;
  unsigned char cout;

  if (argn < 1){
    fprintf(stderr, "This is just to confuse the hacker\n");
    fprintf(stderr, "encrypt: cat file | ./a.out password > efile\n");
    fprintf(stderr, "decrypt: cat efile | ./a.out password D > file\n");
    return 0;
  }
  klen = strlen(key);
  for (i=0; i<N; i++){
      s[i] = (i + klen) % N;
      s_[i] = i;
  }
  for (r=0; r < ROUNDS; r++)
  {
    for (i=0;i<N; i++){
      j = (j + s[i] + key[i % klen]) % N;
      t = s[i] + s[j];
      s[i] = t - s[i];
      s[j] = t - s[j];
    }
  }
  for (r=0; r < ROUNDS; r++)
  {
    for (i=0;i<N; i++){
      j = (j + s_[i] + key[(i+r) % klen]) % N;
      t = s_[i] + s_[j];
      s_[i] = t - s_[i];
      s_[j] = t - s_[j];
    }
  }
  i = s[0];
  j = s[1];
  i2 = s[2];
  j2 = s[N-1];
  argn = 2;
  while ((c = fgetc(stdin)) != -1){
    i = (i + 1) % N;
    j = (j + s[i]) % N;
    i2 = (i2 + s[j]) % N;
    j2 = (j2 + s[i2]) % N;
    t = s_[i] + s_[j];
    s_[i] = t - s_[i];
    s_[j] = t - s_[j];
    t = s[i2] + s[j2];
    s[i2] = t - s[i2];
    s[j2] = t - s[j2];
    if (argn == 2) 
       cout = (c + s_[s[t % N]]) % N;
    else
       cout = (N + c - s_[s[t % N]]) % N;
    if (argn > 2) j ^= c; else j ^= cout;
    printf("%c", cout);    
  }
  fprintf(stderr,"signatue: ");
  for (r=0;r<5;r++){
    i = (i + 1) % N;
    j = (j + s[i]) % N;
    i2 = (i2 + s[j]) % N;
    j2 = (j2 + s[i2]) % N;
    t = s[i2] + s[j2];
    s[i2] = t - s[i2];
    s[j2] = t - s[j2];
    cout = (c + s_[s[t % N]]) % N;
    fprintf(stderr, "%02X", cout);    
  }
  fprintf(stderr, "\n");    
}
      