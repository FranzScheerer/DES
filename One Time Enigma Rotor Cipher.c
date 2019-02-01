Public key: X:  44081111916126392660785044253459069568706513649464
Public key: Y:  45494916568993504055599401243734984564751218543302
Sigature    X:  14398105843367914006375915815452237852459785513539
Sigature    y:  135985827746445904910145460238730928003419562788218

The verification of signature  True

/********
knoppix@Microknoppix:~$ cat ote.c | ./a.out ote.c > oe
calculating hash function: 
D0A09893E76AFE80BFB7F6E20453C4DA9E3386786EA2422256A3B2E22F57B0
Finshed
knoppix@Microknoppix:~$ cat oe | ./a.out ote.c s > oee
calculating hash function: 
D0A09893E76AFE80BFB7F6E20453C4DA9E3386786EA2422256A3B2E22F57B0
Finshed
knoppix@Microknoppix:~$ diff oee ote.c

***********/
/*
 ***********************************************************************
 **                       Franz Scheerer Software                     **
 **                    ONE TIME ENIGMA ROTOR CIPHER                   **       
 ** ote.c -Source file for implementation of a PRNG driven            **
 ** Secure Rotor Cipher wirh sponge like hash function                **
 ** Franz Scheerer Software Spritz Rotor Cipher                       **
 ** Created: 06/28/2016                                               **
 ** Last Update: 06/30/2016                                           **
 ***********************************************************************
 */

/*
 ***********************************************************************
 ** Copyright (C) 2015 - 2018, Scheerer Software, All rights reserved.**
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
 ** Added June 2016 - Sponge like hash function                       **
 ***********************************************************************
 */


/* USAGE:
 * compile: gcc ote.c
 * encrypt: cat data.dat | ./a.out secretX > data.crypt
 * decrypt: cat data.crypt | ./a.out secretX D > data.copy
 *
 * or for encryption/decryption of a whole directory Desktop
 *
 * encrypt: tar -cv Desktop | gzip | ./a.out secretX > filex
 * decrypt: cat filex | ./a.out secretX D | tar -xzv  
 */

#include <stdio.h>
#include <string.h>

#define INITILIZED 0
#define UNCHANGED 1
#define ISCHANGED 0

#define N 256
#define ROUNDS 117  
 
/* 
 *RC4 Cipher:
 *see https://en.wikipedia.org/wiki/RC4
 *
 *   1: i = i + 1
 *   2: j = j + S[i]
 *   3: SWAP(S[i];S[j])
 *   4: z = S[S[i] + S[j]]
 *   5: Return z
 *   see also 
 *   https://people.csail.mit.edu/rivest/pubs/RS14.pdf
 */

/*
 * Pseudo Randdom Number Generator PRNG that turns 
 * the rotors and defines the wireing. 
 * add_j increments state variable j
 * As a result, informtion is absorbed in the state like
 * like water in a sponge. Finally this information
 * is squeezed out as cryptographic secure hash value.
 * https://en.wikipedia.org/wiki/Sponge_function
 */

unsigned char rc4_prng(unsigned char *key, 
                       unsigned int mode, 
                       int add_j) {
/* 
 * Note, a static variable is stored at fixed adress.
 * As a result the values doen't change from one function
 * call to the next.
 */
  static unsigned char S[N];
  static unsigned int i, j = 0;
  int nrepeat,t,klen;
  
  if (mode != INITILIZED)  {
   /* 
    * First initialize, if mode is equal to one, allowing repeated
    * calls of KSA. First initialization runs only once.    
    */
    if (mode == 1){ 
       for (i = 0; i < N; i++){ 
           S[i] = i;
       }
    }
    klen = strlen(key);
    for (nrepeat=0; nrepeat < ROUNDS ; nrepeat++){
      for (i = 0; i < N; i++) {
          j = (j + key[(i + nrepeat) % klen] + S[i]) % N;
          t = S[i]; S[i] = S[j]; S[j]=t;
      }
    }
    i = key[0];
    j = (klen + key[klen-1]) % N;
    for (nrepeat=0; nrepeat < ROUNDS; nrepeat++){
        i = (i + 1) % N;      
        j = (j + S[i]) % N;
        t = S[i]; S[i] = S[j]; S[j]=t;      
    }
    i = S[0]; 
    j = S[1]; 
   } 

   /* INITIALIZED */

   i = (i + 1) % N;
   j = S[(j + S[i]) % N];
   t = S[i]; S[i] = S[j]; S[j] = t;
   j ^= add_j;
   return S[i];        
}
 
int main(int narg, char **argv) {
/* IX is the inverse of X */
  unsigned char S[N];
  unsigned char IR1[N], R1[N];
  unsigned char IR2[N], R2[N];
  unsigned char IR3[N], R3[N];
 /*
  * The rotor positions
  */
  int i1,i2,i3;  
 /*
  * Used for calculation of random reflector
  * (Spiegel S)
  */
  int sx[N];
  unsigned int i, j, k;
  int t, c;
  /* used for sponge hash (add_j) */
  int addR1 = 17; 
 /*
  * Initialize reflector (Spiegel S) and
  * three rotors. The reflector is mounted at
  * the output of the third rotor. 
  * Initialized by Identity
  */
  for (i = 0; i < N; i++){
      S[i] = i;
      R1[i] = i;
      R2[i] = i;
      R3[i] = i;
  }
 /*
  * sx[*] set to unchanged 
  */
  for (i = 0; i < N; i++){
      sx[i] = UNCHANGED;
  }
 /*
  * One command line argument must be set
  * argn equals one means only prpgram name is set. 
  */
  if (narg == 1){
      fprintf(stderr,"ERROR: no password\n");
      return -1;     
  } else {
      rc4_prng("FIRST CALL", 1, 0);      
      rc4_prng(argv[1], strlen(argv[1]), 11); 
      rc4_prng("Pass2", strlen("Pass2"), 13);       
  }

 /* 
  * Fischer-Yates Shuffle for R1, R2 and R3 
  */
  i = N;
  while (i > 1) {
     i = i - 1;
     j = rc4_prng("ENIGMA2", INITILIZED, 17);
     while ( j > i ){
       j = rc4_prng("ENIGMA2", INITILIZED, 42);
     }
     t = R1[i]; R1[i] = R1[j]; R1[j] = t;
  } 
  i = N;  
  while (i > 1) {
     i = i - 1;
     j = rc4_prng("ENIGMA2", INITILIZED, 8);
     while ( j > i ){
       j = rc4_prng("ENIGMA2", INITILIZED, 15);
     }
     t = R2[i]; R2[i] = R2[j]; R2[j] = t;
  } 
  i = N;  
  while (i > 1) {
     i = i - 1;
     j = rc4_prng("ENIGMA2", INITILIZED, 3);
     while ( j > i ){
       j = rc4_prng("ENIGMA2", INITILIZED, 33);
     }
     t = R3[i]; R3[i] = R3[j]; R3[j] = t;
  }
  /* Random reflector S (Spiegel) */
  i = N;  
  while (i > 1) {
     i = i - 1;
     if (sx[i] == UNCHANGED){
       j = rc4_prng("ENIGMA2", INITILIZED, 23);
       while ( j >= i || (sx[j] == ISCHANGED) ){
         j = rc4_prng("ENIGMA2", INITILIZED, 13);
       }
       t = S[i]; S[i] = S[j]; S[j] = t;
       sx[j] = ISCHANGED; 
     }
  }
 /* 
  * calulate the inverse rotators 
  */
  for (i = 0; i < N; i++){
      IR1[R1[i]] = i;
      IR2[R2[i]] = i;
      IR3[R3[i]] = i;
  }
 /* 
  * Initialize starting positions of the 
  * three rotors before encryption.
  */
  i1 = rc4_prng("ENIGMA2", INITILIZED, 1);
  i2 = rc4_prng("ENIGMA2", INITILIZED, 2);
  i3 = rc4_prng("ENIGMA2", INITILIZED, 3);
  
 /* 
  * main-loop read and enrypt/decrypt byte by byte from stdin to stdout
  */
  while ( (c = fgetc(stdin)) != -1 )
  {
     /*
      * tempoary variables 
      */
      int t0,t1,t2,t3,t4,t5,t6,t7;
     /* 
      * calculate random rotor positions
      * equal for encryption and decryption
      * but depending on the message encrypted
      */
      i1 = (i1 + 1) % N;
      i2 = (i2 + R1[i1] + addR1) % N;
      i3 = (i3 + R1[i2] + addR1) % N;
     /* 
      * The wireing in rotor one is changed for
      * each byte being encrypted. Two virtual
      * connections are exchanged.
      */
      t0 = R1[i1]; 
      R1[i1] = R1[i3];
      R1[i3] = t0;
      IR1[R1[i1]] = i1;
      IR1[R1[i3]] = i3;
     /* 
      * The message is finally encrypted by random 
      * sequence, so that a byte value might be 
      * replaced by itself. The double encryption is
      * extremely secure.
      * Then decrypting the second encryption is
      * first inverted.
      */
      if (narg > 2)               /* decrypt */
         c ^= R1[ rc4_prng("ENIGMA2", INITILIZED, addR1) ];

      t1 = R1[(i1 + c) % N];
      t2 = R2[(t1 + i2) % N];
      t3 = R3[(t2 + i3) % N];
      t4 = S[t3];
      t5 = (N + IR3[t4] - i3) % N; /* add N to avoid negative value */
      t6 = (N + IR2[t5] - i2) % N;
      t7 = (N + IR1[t6] - i1) % N;

      /* output encrypted/decrypted byte */

      if (narg == 2){ 
         /* modified by output (encrypt) */   
         t0 = addR1;  
         addR1 ^= t7;
         /* additional encryption by random sequence (encrypt) */      
         t7 ^= R1[ rc4_prng("ENIGMA2", INITILIZED, t0) ];
      } else { 
         addR1 ^= c;   /* modified by input (decrypt) */
      }
      /* print output */
      printf("%c", t7);

     } /* end main-loop */

     fprintf(stderr,"calculating hash function: \n");
     /*
      * addR1 must be added, since otherwise the last character
      * would not change the checksum.
      */ 
     i1 = (i1 + addR1) % N;
     for (c=0; c<32; c++){
        fprintf(stderr,"%0X", rc4_prng("ENIGMA2", INITILIZED, R1[(i1+i2+i3) % N])); 
       /* 
        * No need to change R1 again here. 
        */
        i1 = (i1 + 1) % N;
        i2 = (i2 + R1[i1] + addR1) % N;
        i3 = (i3 + R1[i2] + addR1) % N;
     }
     fprintf(stderr,"\nFinshed\n");
}
