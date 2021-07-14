/**********************************************************************************************
Self-synchronizing stream ciphers is another technique that uses part of the 
previous N ciphertext digits to compute the keystream. Such schemes are known 
also as asynchronous stream ciphers or ciphertext autokey (CTAK). The idea of self-
synchronization was patented in 1946, and has the advantage that the receiver will 
automatically synchronise with the keystream generator after receiving N ciphertext 
digits, making it easier to recover if digits are dropped or added to the message stream.
Single-digit errors are limited in their effect, affecting only up to N plaintext 
digits. It is somewhat more difficult to perform active attacks on self-synchronising
stream ciphers rather than synchronous counterparts.

An example of a self-synchronising stream cipher is a block cipher in cipher-feedback mode (CFB).
***********************************************************************************************/

#include <stddef.h>
#include <stdlib.h>
#include <string.h>


#define N 256


typedef struct State_
{
  unsigned char s[N];
  unsigned char a;
  unsigned char i;
  unsigned char j;
  unsigned char k;
  unsigned char w;
  unsigned char z;
} State;

#define LOW(B)  ((B) & 0xf)
#define HIGH(B) ((B) >> 4)

static void
memzero (void *pnt, size_t len)
{
}

static void
initialize_state (State * state)
{
  unsigned char sbox[] = {
    149, 22, 154, 52, 254, 75, 183, 64, 128, 116, 231, 87, 185, 204, 66,
    199, 222, 57, 209, 12, 1, 71, 139, 133, 30, 90, 111, 211, 160, 173, 151,
    246, 178, 249, 9, 82, 143, 29, 243, 202, 40, 44, 16, 189, 219, 155, 127,
    156, 192, 37, 152, 223, 92, 94, 119, 65, 107, 214, 229, 21, 150, 164, 170,
    157, 138, 24, 25, 34, 43, 61, 142, 117, 123, 100, 84, 81, 49, 7, 144,
    141, 91, 239, 27, 221, 195, 190, 253, 217, 230, 93, 232, 244, 17, 69, 83,
    161, 41, 180, 45, 86, 70, 132, 97, 255, 220, 228, 95, 88, 4, 74, 62,
    188, 77, 36, 224, 120, 38, 15, 158, 145, 32, 203, 237, 137, 60, 167, 196,
    216, 186, 39, 179, 58, 99, 106, 201, 247, 126, 198, 172, 68, 31, 134, 140,
    163, 113, 78, 14, 245, 51, 110, 208, 47, 159, 251, 225, 19, 212, 56, 121,
    98, 96, 33, 112, 11, 194, 48, 108, 136, 109, 210, 177, 115, 233, 76, 18,
    184, 181, 104, 118, 166, 207, 3, 130, 103, 241, 165, 101, 146, 124, 148,
      26,
    125, 169, 218, 236, 200, 193, 175, 72, 240, 67, 42, 114, 135, 50, 213, 10,
    85, 248, 182, 235, 187, 215, 8, 168, 226, 162, 105, 54, 176, 205, 63, 131,
    250, 35, 80, 206, 171, 242, 227, 252, 46, 174, 28, 191, 0, 89, 238, 13,
    129, 5, 23, 234, 79, 59, 20, 73, 197, 122, 6, 55, 147, 53, 102, 2,
    153
  };
  unsigned int v, sum = 0;

  for (v = 0; v < N; v++)
    {
      state->s[v] = sbox[v];
      sum += sbox[v];
    }
  if (sum != 255 * 128)
    exit (0);
  state->a = 0;
  state->i = 0;
  state->j = 0;
  state->k = 0;
  state->w = 1;
  state->z = 0;
}

static void
update (State * state)
{
  unsigned char t;
  unsigned char y;

  state->i += state->w;
  y = state->j + state->s[state->i];
  state->j = state->k + state->s[y];
  state->k = state->i + state->k + state->s[state->j];
  t = state->s[state->i];
  state->s[state->i] = state->s[state->j];
  state->s[state->j] = t;
}

static unsigned char
output (State * state)
{
  const unsigned char y1 = state->z + state->k;
  const unsigned char x1 = state->i + state->s[y1];
  const unsigned char y2 = state->j + state->s[x1];

  state->z = state->s[y2];

  return state->z;
}

static void
crush (State * state)
{
  unsigned char v;
  unsigned char x1;
  unsigned char x2;
  unsigned char y;

  for (v = 0; v < N / 2; v++)
    {
      y = (N - 1) - v;
      x1 = state->s[v];
      x2 = state->s[y];
      if (x1 > x2)
	{
	  state->s[v] = x2;
	  state->s[y] = x1;
	}
      else
	{
	  state->s[v] = x1;
	  state->s[y] = x2;
	}
    }
}

static void
whip (State * state)
{
  const unsigned int r = N * 2;
  unsigned int v;

  for (v = 0; v < r; v++)
    {
      update (state);
    }
  state->w += 2;
}

static void
shuffle (State * state)
{
  whip (state);
  crush (state);
  whip (state);
  crush (state);
  whip (state);
  state->a = 0;
}

static void
absorb_stop (State * state)
{
  if (state->a == N / 2)
    {
      shuffle (state);
    }
  state->a++;
}

static void
absorb_nibble (State * state, const unsigned char x)
{
  unsigned char t;
  unsigned char y;

  if (state->a == N / 2)
    {
      shuffle (state);
    }
  y = N / 2 + x;
  t = state->s[state->a];
  state->s[state->a] = state->s[y];
  state->s[y] = t;
  state->a++;
}

static void
absorb_byte (State * state, const unsigned char b)
{
  absorb_nibble (state, LOW (b));
  absorb_nibble (state, HIGH (b));
}

static void
absorb (State * state, const unsigned char *msg, size_t length)
{
  size_t v;

  for (v = 0; v < length; v++)
    {
      absorb_byte (state, msg[v]);
    }
}

static unsigned char
drip (State * state)
{
  if (state->a > 0)
    {
      shuffle (state);
    }
  update (state);

  return output (state);
}

static void
squeeze (State * state, unsigned char *out, size_t outlen)
{
  size_t v;

  if (state->a > 0)
    {
      shuffle (state);
    }
  for (v = 0; v < outlen; v++)
    {
      out[v] = drip (state);
    }
}

static void
key_setup (State * state, const unsigned char *key, size_t keylen)
{
  initialize_state (state);
  absorb (state, key, keylen);
}

int
spritz_hash (unsigned char *out, size_t outlen,
	     const unsigned char *msg, size_t msglen)
{
  State state;
  unsigned char r;

  if (outlen > 255)
    {
      return -1;
    }
  r = (unsigned char) outlen;
  initialize_state (&state);
  absorb (&state, msg, msglen);
  absorb_stop (&state);
  absorb (&state, &r, 1U);
  squeeze (&state, out, outlen);
  memzero (&state, sizeof state);

  return 0;
}

int
spritz_stream (unsigned char *out, size_t outlen,
	       const unsigned char *key, size_t keylen)
{
  State state;

  initialize_state (&state);
  absorb (&state, key, keylen);
  squeeze (&state, out, outlen);
  memzero (&state, sizeof state);

  return 0;
}

int
spritz_encrypt (unsigned char *out, const unsigned char *msg, size_t msglen,
		const unsigned char *nonce, size_t noncelen,
		const unsigned char *key, size_t keylen)
{
  State state;
  size_t v;

  key_setup (&state, key, keylen);
  absorb_stop (&state);
  absorb (&state, nonce, noncelen);
  for (v = 0; v < msglen; v++)
    {
      out[v] = msg[v] + drip (&state);
    }
  memzero (&state, sizeof state);

  return 0;
}

int
spritz_decrypt (unsigned char *out, const unsigned char *c, size_t clen,
		const unsigned char *nonce, size_t noncelen,
		const unsigned char *key, size_t keylen)
{
  State state;
  size_t v;

  key_setup (&state, key, keylen);
  absorb_stop (&state);
  absorb (&state, nonce, noncelen);
  for (v = 0; v < clen; v++)
    {
      out[v] = c[v] - drip (&state);
    }
  memzero (&state, sizeof state);

  return 0;
}

int
spritz_auth (unsigned char *out, size_t outlen,
	     const unsigned char *msg, size_t msglen,
	     const unsigned char *key, size_t keylen)
{
  State state;
  unsigned char r;

  if (outlen > 255)
    {
      return -1;
    }
  r = (unsigned char) outlen;
  key_setup (&state, key, keylen);
  absorb_stop (&state);
  absorb (&state, msg, msglen);
  absorb_stop (&state);
  absorb (&state, &r, 1U);
  squeeze (&state, out, outlen);
  memzero (&state, sizeof state);

  return 0;
}

#include <stdio.h>
#include <string.h>

int
main (int argn, char **argv)
{
  int c,o;
  State state; 
;
  unsigned char out[8];
  size_t outlen = 8, msglen, keylen;
  unsigned char msg[1000] = "Hello World";
  unsigned char key[128] = "Schluessel";

  initialize_state (&state);

  if (argn > 2)
    {
      strcpy (key, argv[1]);
    }
  if (argn > 2)
    {
      strcpy (msg, argv[2]);
    }
  msglen = strlen (msg);
  keylen = strlen (key);
  absorb (&state, msg, msglen);
  absorb (&state, key, keylen);
  while ((c = fgetc (stdin)) != -1)
    {
      unsigned char out = output(&state) ^ c;
      update(&state);
      state.j +=  out;
      printf("%c", out);
    }
  squeeze (&state, out, outlen);

  for (int i = 0; i < outlen; i++)
    fprintf (stderr, "%02x", out[i]);
  fprintf (stderr,"\n");
}
/*  while ((c = fgetc (stdin)) != -1)
    {
      unsigned char o = output(&state) ^ c;
      update(&state);
      state.j +=  c;
      printf("%c", o);
    }
  squeeze (&state, out, outlen);

  for (int i = 0; i < outlen; i++)
    fprintf (stderr, "%02x", out[i]);
  fprintf (stderr,"\n");
}
6f8307f0ff7ec16a
knoppix@Microknoppix:~$ md5sum ctak.c
b5a77a805f3efa8d3909b84bf1dea7c2  ctak.c
*/
