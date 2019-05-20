// Standardeingabe (stdin) und Ausgabe (stdout)
// und Fehleranzeige (stderr)
#include <stdio.h>
// Zur Bestimmung der Länge des Passwort benötigt
// Kopfdatei für Zeichenketten (Strings)
#include <string.h>
// N ist die Anzahl der Zeichen im Standardalphabet der EDV
#define N 256
// Zahl der Wiederholungen
#define ROUNDS 3

// Die Ausführung befinnt hier wie immer in C mit der Funktion "main()") 
int main(int argn, char **argv){
// Im Vergleich zu RC4 gibt es eine weitere S-Box S_
//
  int s[N], s_[N];
  int klen,t,i,j=0;
  int i2,j2;
  int r, c;
  // Das verschlüsselte Zeichen
  unsigned char cout;
// Das Programm soll mit mindestens einem Parameter plus Programmname in argv[0]
// aufgeruden werden. Der Parameter ist das Passwort.
// Wird ein weiterer Parameter angegeben, erfolgt die Entschlüsselung statt
// der Verschlüsselung.
// Der Prgrammname sei "a.out", der Standardname ohne Parameter -o bei gcc.
  if (argn < 2){
    fprintf(stderr, "encrypt: cat file | ./a.out password > efile\n");
    fprintf(stderr, "decrypt: cat efile | ./a.out password D > file\n");
    return 0;
  }
// Die Länge des Passworts
  klen = strlen(argv[1]);
// Anfangsbesetung der S-Boxen (Permutationen)
  for (i=0; i<N; i++){
      s[i] = (i + klen) % N;
      s_[i] = i;
  }
// Mit drei Wiederhollungen. 
// Mischen von S-Box s.
  for (r=0; r < ROUNDS; r++)
  {
    for (i=0;i<N; i++){
      j = (j + s[i] + argv[1][i % klen]) % N;
      t = s[i] + s[j];
      s[i] = t - s[i];
      s[j] = t - s[j];
    }
  }
// Mischen von S-Box s_.
  for (r=0; r < ROUNDS; r++)
  {
    for (i=0;i<N; i++){
      j = (j + s_[i] + argv[1][(i+r) % klen]) % N;
      t = s_[i] + s_[j];
      s_[i] = t - s_[i];
      s_[j] = t - s_[j];
    }
  }
  i = s[0];
  j = s[1];
  i2 = s[2];
  j2 = s[N-1];
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

// Zwei unterschiedliche Nachrichten mit identischen 
// Hash sind praktisch ausgeschlossen. Sie können
// auch von einem Hacker nicht konstruiert werden
  fprintf(stderr,"hash (256 bits):\n ");
  for (r=0;r<32;r++){
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
      