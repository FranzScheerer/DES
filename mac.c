/*
 **********************************************************************
 ** mac.c Source file for stream cipher based keyed hash             **
 ** Franz Scherer Software  Perfect Stream Cipher based Hash         **
 ** Created: 09/04/2016                                              **
 **********************************************************************
 */

/*
 **********************************************************************
 ** Copyright (C) 2016, Scheerer Software, All rights reserved.      **
 **                                                                  **
 ** License to copy and use this software is granted provided that   **
 ** it is identified as the "Franz Scheerer Software, Perfect Stream **
 ** Cipher based Hash Algorithm" in all material mentioning or       ** 
 ** referencing this software or this function.                      **
 **                                                                  **
 ** License is also granted to make and use derivative works         **
 ** provided that such works are identified as "derived from         **
 ** Franz Scheerer Software Perfect Stream Cipher Algorithm" in all  **
 ** material mentioning or referencing the derived work.             **
 **                                                                  **
 ** Franz Scheerer Software makes no representations concerning      **
 ** either the merchantability of this software or the suitability   **
 ** of this software for any particular purpose.  It is provided "as **
 ** is" without express or implied warranty of any kind.             **
 **                                                                  **
 ** These notices must be retained in any copies of any part of this **
 ** documentation and/or software.                                   **
 **********************************************************************
 */

#include <stdio.h>
#include <string.h>


#define N 32
#define ROUNDS 9999

int mac(char *password){
  unsigned int s[512];
  int t,i,ja,jb,jc,jd,je,jf,jg,jh;
  int c,r;
  int len = strlen(password);
   
  for (i=0;i < 512; i++) 
     s[i] = (i + len) % 512;
  ja = 0;
  for (r=0; r< ROUNDS; r++) for (i=0;i < 512; i++){ 
     ja = (ja + s[i] + password[(i + r) % len]) % 512;
     t = s[ja]; s[ja] = s[i]; s[i] = t;
  }
  i = jb = jc = jd = je = jf = jg = jh = 0;

  while ( (c = fgetc(stdin)) != -1 )
  {
    for (r=0;r<4;r++){   
      i = (i + 1) % 512;
      ja = (jh + s[(ja + s[i]) % 512]) % 512;
      jb = (jb + s[ja]) % 512;
      jc = (jc + s[jb]) % 512;
      jd = (jd + s[jc]) % 512;
      je = (je + s[jd]) % 512;
      jf = (jf + s[je]) % 512;
      jg = (jg + s[jf]) % 512;
      jh = (jh + s[jg]) % 512;
      t = s[jc]; s[jc] = s[i]; s[i] = t;
      if (r==1) 
        ja = (ja + (c ^ t)) % 512;
      else
        ja = (ja ^ (c ^ t)) % 512;
    }
  }
  for (c=0;c<512;c++){
     i = (i + 1) % 512;
     jb = s[(jb + s[i]) % 512];
     t = s[jb]; s[jb] = s[i]; s[i] = t;
  }
  for (c=0;c<N;c++){
    i = (i + 1) % 512;
    ja = (ja + s[i]) % 512;
    jb = (jb + s[ja]) % 512;
    jc = (jc + s[jb]) % 512;
    jd = (jc + s[jc]) % 512;
    je = (jc + s[jd]) % 512;
    jf = (jc + s[je]) % 512;
    jg = (jc + s[jf]) % 512;
    jh = (jh + s[jg]) % 512;
    t = s[jh]; s[jh] = s[i]; s[i] = t;
    printf("%02x", t & 0xFF);
  }
  return 0;  
}

int main(int argn, char **argv){
  printf("Usage: gcc mac.c\n");
  printf("Calculate mac of file: cat file | ./a.out password\n");

  printf("Calculating mac ... \n");

  if (argn > 1) mac(argv[1]);

  printf("\n\n");

}

