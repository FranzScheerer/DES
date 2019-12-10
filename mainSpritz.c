#include <stddef.h>
#include <string.h>

typedef struct Spritz_ {
    unsigned char s[256];
    unsigned char a;
    unsigned char i;
    unsigned char j;
    unsigned char k;
    unsigned char w;
    unsigned char z;
} Spritz;

static void
initialize_state(Spritz *state)
{
    unsigned int v;

    for (v = 0; v < 256; v++) {
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
update(Spritz *state)
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
output(Spritz *state)
{
    const unsigned char y1 = state->z + state->k;
    const unsigned char x1 = state->i + state->s[y1];
    const unsigned char y2 = state->j + state->s[x1];

    state->z = state->s[y2];

    return state->z;
}

static void
whip(Spritz *state)
{
    unsigned int       v;

    for (v = 0; v < 512; v++) {
        update(state);
    }
    state->w += 2;
}

static void
shuffle(Spritz *state)
{
    whip(state);
    state->a = 0;
}


static void
absorb_nibble(Spritz *state, const unsigned char x)
{
    unsigned char t;
    unsigned char y;

    if (state->a == 128) {
        shuffle(state);
    }
    y = 128 + x;
    t = state->s[state->a];
    state->s[state->a] = state->s[y];
    state->s[y] = t;
    state->a++;
}

static void
absorb_byte(Spritz *state, const unsigned char b)
{
    absorb_nibble(state, b & 0x0f);
    absorb_nibble(state, b >> 4);
}

static void
absorb(Spritz *state, const unsigned char *msg, size_t length)
{
    size_t v;

    for (v = 0; v < length; v++) {
        absorb_byte(state, msg[v]);
    }
}

static unsigned char
drip(Spritz *state)
{
    if (state->a > 0) {
        shuffle(state);
    }
    update(state);

    return output(state);
}

static void
squeeze(Spritz *state, unsigned char *out, size_t outlen)
{
    size_t v;

    if (state->a > 0) {
        shuffle(state);
    }
    for (v = 0; v < outlen; v++) {
        out[v] = drip(state);
    }
}
#include<stdio.h>
int main(int argn, char* argv[]){
    Spritz state;
    unsigned char out[33]; 
    initialize_state(&state);
    if (argn > 1) {
       for (int i=0; i<strlen(argv[1]); i++)
          absorb_byte(&state, argv[1][i]);
       out[33] = 0;
       squeeze(&state, out, 32);
       for (int i=0; i < 32; i++) 
         printf("%02x", out[i]);
    }
    printf("\n");
}    
