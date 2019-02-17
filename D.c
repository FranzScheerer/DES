/**********************************************************************
 ** spritzenigma.c Source file for implementation of a PRNG driven   **
 ** Secure Rotor Cipher                                              **
 ** Franz Scherer Software Spritz Rotor Cipher                       **
 ** Created: 07/11/2015                                              **
 **********************************************************************
 */

/*
 ***********************************************************************
 ** Copyright (C) 2015 - 2016, Scheerer Software, All rights reserved.**
 **                                                                   **
 ** License to copy and use this software is granted provided that    **
 ** it is identified as the "Franz Scheerer Software, Rotor           **
 ** Cipher Algorithm" in all material mentioning or referencing this  **
 ** software or this function.                                        **
 **                                                                   **
 ** License is also granted to make and use derivative works          **
 ** provided that such works are identified as "derived from          **
 ** Franz Scheerer Software Rotor Cipher Algorithm" in all            **
 ** material mentioning or referencing the derived work.              **
 **                                                                   **
 ** Franz Scheerer Software makes no representations concerning       **
 ** either the merchantability of this software or the suitability    **
 ** of this software for any particular purpose.  It is provided "as  **
 ** is" without express or implied warranty of any kind.              **
 **                                                                   **
 ** These notices must be retained in any copies of any part of this  **
 ** documentation and/or software.                                    **
 ** June 2016 - Now with Sponge hash                                  **
 ***********************************************************************
 */


/*
 * compile: gcc spritzenigma.c
 * encrypt: cat data.dat | ./a.out secretX > data.crypt
 * decrypt: cat data.crypt | ./a.out secretX D > data.copy
 */

#include <stdio.h>
#include <string.h>
 
/* Spritz Cipher, slightly modified 

Spritz:
(from https://www.schneier.com/blog/archives/2014/10/spritz_a_new_rc.html)

    1: i = i + w
    2: j = k + S[j + S[i]]
    2a: k = i + k + S[j]
    3: SWAP(S[i];S[j])
    4: z = S[j + S[i + S[z + k]]]
    5: Return z
*/
unsigned char 
spritz(unsigned char *key, unsigned int key_length,
       int add_j) {
  static unsigned char S[256];
  static unsigned int i,j,k,w,z;
  int nrepeat,t;
  
  if (key_length > 0) /* initialize, if key_length greater than zero */
  {
    if (key_length == 1) 
       for (i = 0; i < 256; i++) S[i] = i;
    j = 0;
    for (nrepeat=0; nrepeat<3; nrepeat++){
      for (i = 0; i < 256; i++) {
          j = (j + key[(i + nrepeat) % key_length] + S[i]) % 256;
          t = S[i]; S[i] = S[j]; S[j]=t;
      }
    }
    i = key[0] % 256;
    j = (key_length + key[key_length-1]) % 256;
    for (nrepeat=0; nrepeat<999; nrepeat++){
        i = (i + 1) % 256;      
        j = (j + S[i]) % 256;
        t = S[i]; S[i] = S[j]; S[j]=t;      
    }
    i = S[42]; 
    j = S[0]; k = S[8];
    w = 2*S[15] + 1;
    z = S[47] + S[11];
   } /* end initialize */

   i = (i + w) % 256;
   j = (k + S[j + S[i]]) % 256;
   k = (i + k + S[j]) % 256;
   t = S[i]; S[i] = S[j]; S[j]=t;
   z = S[(j + S[(i + S[(z + k) % 256]) % 256]) % 256];
   j += add_j;
   return z;        
}
 
 
int main(int narg, char **argv) {
  unsigned char IS[256],  S[256];
  unsigned char IR1[256], R1[256];
  unsigned char IR2[256], R2[256];
  unsigned char IR3[256], R3[256];
  unsigned int i, j, k;
  int t, c;
  int addR1 = 17;

  for (i = 0; i < 256; i++){
      S[i] = i;
      R1[i] = i;
      R2[i] = i;
      R3[i] = i;
  }
      spritz("1", strlen("1"),0);      
      spritz("ERROR: no password\n", strlen("ERROR: no password\n"),0); 
      spritz("Pass2", strlen("Pass2"),0);       
  
  i = 256;  
  while (i > 1) {
     i = i - 1;
     j = spritz("ENIGMA2", 0, 0);
     while ( j > i ){
       j = spritz("ENIGMA2", 0, 0);
     }
     t = S[i]; S[i] = S[j]; S[j] = t;
  } 
  i = 256;  
  while (i > 1) {
     i = i - 1;
     j = spritz("ENIGMA2", 0, 0);
     while ( j > i ){
       j = spritz("ENIGMA2", 0, 0);
     }
     t = R1[i]; R1[i] = R1[j]; R1[j] = t;
  } 
  i = 256;  
  while (i > 1) {
     i = i - 1;
     j = spritz("ENIGMA2", 0, 0);
     while ( j > i ){
       j = spritz("ENIGMA2", 0, 0);
     }
     t = R2[i]; R2[i] = R2[j]; R2[j] = t;
  } 
  i = 256;  
  while (i > 1) {
     i = i - 1;
     j = spritz("ENIGMA2", 0, 0);
     while ( j > i ){
       j = spritz("ENIGMA2", 0, 0);
     }
     t = R3[i]; R3[i] = R3[j]; R3[j] = t;
  }

  for (i = 0; i < 256; i++){
      IS[S[i]] = i;
      IR1[R1[i]] = i;
      IR2[R2[i]] = i;
      IR3[R3[i]] = i;
      /* printf("%d %d %d %d\n", S[i],R1[i],R2[i],R3[i]); */
  }
 
     while ((c = fgetc(stdin)) != -1){
        int t,i1,i2,i3;
        i1 = (addR1 + spritz("ENIGMA2", 0, addR1)) % 256;
        i2 = spritz("ENIGMA2", 0, addR1);
        i3 = spritz("ENIGMA2", 0, addR1);
        t = R3[i1]; 
        R3[i1] = R3[i2];
        R3[i2] = t;
        IR3[R3[i1]] = i1;
        IR3[R3[i2]] = i2;
        {
            int t1,t2,t3,t4;
            t4 = c;
            t3 = IS[t4];
            t2 = (256 + IR3[t3] - i3) % 256;
            t1 = (256 + IR2[t2] - i2) % 256;
            printf("%c", (256 + IR1[t1] - i1) % 256);
            addR1 = t4;
        }
     }
     fprintf(stderr,"calculating hash function: \n");
     fprintf(stderr,"%X", spritz("ENIGMA2", 0, addR1));
     for (c=0; c<300; c++){
        spritz("ENIGMA2", 0, 0);
        if (c > 266)
          fprintf(stderr,"%X", spritz("ENIGMA2", 0, 0));
     }
     fprintf(stderr,"\nFinshed\n");

}
