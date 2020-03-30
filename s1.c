#include <stddef.h>
#include <string.h>


#define N 256

typedef struct State_ {
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
initialize_state(State *state)
{
    unsigned int v;

    for (v = 0; v < N; v++) {
        state->s[v] = (unsigned char) v;
    }
    state->a = 0;
    state->i = 0;
    state->j = 0;
    state->k = 0;
    state->w = 1;
    state->z = 0;
}

static void
update(State *state)
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
output(State *state)
{
    const unsigned char y1 = state->z + state->k;
    const unsigned char x1 = state->i + state->s[y1];
    const unsigned char y2 = state->j + state->s[x1];

    state->z = state->s[y2];

    return state->z;
}


static void
whip(State *state)
{
    const unsigned int r = N * 2;
    unsigned int       v;

    for (v = 0; v < r; v++) {
        update(state);
    }
    state->w += 2;
}

static void
shuffle(State *state)
{
    whip(state);
    whip(state);
    state->a = 0;
}

static void
absorb_nibble(State *state, const unsigned char x)
{
    unsigned char t;
    unsigned char y;

    if (state->a == N / 2) {
        shuffle(state);
    }
    y = N / 2 + x;
    t = state->s[state->a];
    state->s[state->a] = state->s[y];
    state->s[y] = t;
    state->a++;
}

static void
absorb_byte(State *state, const unsigned char b)
{
    absorb_nibble(state, LOW(b));
    absorb_nibble(state, HIGH(b));
}


static unsigned char
drip(State *state)
{
    if (state->a > 0) {
        shuffle(state);
    }
    update(state);

    return output(state);
}

static void
squeeze(State *state, unsigned char *out, size_t outlen)
{
    size_t v;

    if (state->a > 0) {
        shuffle(state);
    }
    for (v = 0; v < outlen; v++) {
        out[v] = drip(state);
    }
}


#include <stdio.h>
int main(){
  int i,c;
  char out[32];  
  State state;
  initialize_state(&state);
  while ((c = fgetc(stdin)) != -1){
     absorb_byte(&state, c);
  }
  squeeze(&state, out, 32);

  for (i=0;i<32;i++)
     fprintf(stdout, "%02X", (unsigned char)out[i]);
  fprintf(stdout, "\n");

  return 0;
}