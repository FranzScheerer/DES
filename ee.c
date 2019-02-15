#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
//#include <getopt.h> 

uint64_t kx[64] = {15541898472998496256UL,9742394704947216384UL,1179782310628909056UL,
3083609941704052736UL,1319800878577229824UL,3421426469963220992UL,
3485005304174794752UL,4313196360192434176UL,8006886543861346304UL,
11126723444717156352UL,17275337824244322304UL,11506993556996247552UL,
5431207704280184832UL,350290758795798528UL,11694452332012478464UL,
7722881041058809856};

// 
// Implementation of DES coded by:
//     - David Wong, moi@davidwong.fr
//     - Jacques Monin, jacques.monin@u-bordeaux.fr
//     - Hugo Bonnin, hugo.bonnin@u-bordeaux.fr
//     - Franz Scheerer scheerer.software@gmail.com
//


#define FIRSTBIT 0x8000000000000000 

void addbit(uint64_t *block, uint64_t from,
            int position_from, int position_to);

// Initial and Final Permutations
void Permutation(uint64_t* data, bool initial);


void rounds(uint64_t *data, uint64_t key);

// Permutation tables
const int InitialPermutation[64] = { 
21, 10, 31, 32, 40, 30, 16, 8, 33, 63, 
57, 41, 34, 58, 51, 45, 18, 19, 56, 20, 
49, 46, 3, 13, 54, 39, 44, 7, 48, 9, 
38, 14, 55, 59, 24, 35, 12, 61, 17, 37, 
23, 26, 11, 42, 4, 1, 64, 27, 52, 2, 
22, 25, 15, 62, 5, 60, 36, 43, 6, 50, 
29, 47, 28, 53
};
const int FinalPermutation[64] = { 
46, 50, 23, 45, 55, 59, 28, 8, 30, 2, 
43, 37, 24, 32, 53, 7, 39, 17, 18, 20, 
1, 51, 41, 35, 52, 42, 48, 63, 61, 6, 
3, 4, 9, 13, 36, 57, 40, 31, 26, 5, 
12, 44, 58, 27, 16, 22, 62, 29, 21, 60, 
15, 49, 64, 25, 33, 19, 11, 14, 34, 56, 
38, 54, 10, 47
};

// Rounds tables
/*
const int DesExpansion[48] = {
    1,  1,  2,  3,  4,  5,  4,  5,
     6,  7,  8,  9,  8,  9, 10, 11,
    12, 13, 12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21, 20, 21,
    22, 23, 24, 25, 24, 25, 26, 27,
    28, 29, 28, 29, 30, 31, 32, 32
};
*/ 
const int DesExpansion[48] = {
7, 24, 26, 32, 9, 20, 12, 20, 17, 29, 3, 28,
 13, 4, 29, 13, 8, 17, 12, 25, 21, 23, 18, 1, 
10, 24, 14, 5, 1, 16, 11, 30, 9, 25, 4, 2, 22,
 19, 21, 8, 32, 16, 27, 15, 5, 6, 28, 31
};

 
const int DesSbox[8][4][16] = {
   {
   {15, 7, 0, 4, 6, 8, 10, 5, 12, 14, 3, 1, 9, 2, 13, 11},
   {14, 1, 2, 10, 7, 0, 11, 15, 5, 13, 4, 6, 8, 9, 12, 3},
   {0, 3, 5, 12, 14, 9, 7, 11, 6, 4, 8, 1, 2, 13, 10, 15},
   {10, 11, 0, 9, 4, 5, 1, 8, 3, 12, 7, 2, 14, 6, 13, 15},
   },
 
   {
   {10, 0, 3, 2, 8, 9, 5, 11, 7, 6, 1, 15, 14, 4, 13, 12},
   {13, 9, 7, 1, 14, 10, 4, 11, 5, 8, 15, 2, 12, 6, 0, 3},
   {7, 4, 6, 11, 8, 10, 9, 2, 3, 15, 14, 5, 12, 1, 13, 0},
   {9, 15, 6, 3, 13, 11, 5, 14, 1, 12, 10, 8, 7, 2, 0, 4},
   },
 
   {
   {10, 5, 12, 9, 1, 4, 0, 8, 2, 7, 3, 11, 6, 14, 15, 13},
   {7, 6, 4, 14, 9, 1, 5, 12, 0, 3, 11, 15, 8, 10, 13, 2},
   {8, 3, 4, 10, 7, 1, 2, 0, 5, 14, 15, 13, 9, 6, 12, 11},
   {11, 13, 4, 1, 12, 6, 15, 8, 2, 9, 10, 7, 0, 3, 5, 14},
   },
 
   {
   {1, 8, 9, 7, 6, 14, 15, 4, 5, 13, 2, 3, 11, 12, 10, 0},
   {9, 4, 14, 15, 6, 11, 12, 7, 13, 5, 10, 2, 1, 0, 8, 3},
   {7, 13, 10, 15, 0, 3, 6, 9, 5, 12, 2, 4, 11, 8, 14, 1},
   {3, 8, 2, 6, 1, 5, 9, 13, 12, 4, 11, 15, 0, 10, 7, 14},
   },
 
   {
   {3, 8, 2, 6, 1, 5, 9, 13, 12, 4, 11, 15, 0, 10, 7, 14},
   {0, 2, 7, 6, 11, 1, 4, 3, 15, 8, 10, 5, 14, 12, 13, 9},
   {11, 13, 14, 0, 12, 5, 8, 15, 1, 2, 10, 3, 9, 7, 6, 4},
   {11, 6, 8, 4, 2, 1, 10, 5, 7, 14, 9, 0, 15, 12, 3, 13},
   },
 
   {
   {5, 15, 10, 14, 9, 4, 11, 0, 7, 8, 3, 6, 12, 13, 2, 1},
   {1, 5, 11, 9, 4, 13, 6, 3, 7, 14, 8, 2, 15, 12, 10, 0},
   {9, 8, 6, 7, 0, 1, 4, 10, 14, 3, 11, 5, 15, 13, 2, 12},
   {14, 7, 1, 9, 0, 10, 11, 3, 8, 2, 4, 6, 5, 13, 15, 12},
   },
 
   {
   { 1, 3, 2, 13, 4, 6, 0, 8, 7, 12, 10, 5, 15, 9, 11, 14},
   { 9, 2, 15, 1, 3, 13, 12, 14, 6, 11, 10, 5, 0, 4, 8, 7},
   { 9, 2, 15, 1, 3, 13, 12, 14, 6, 11, 10, 5, 0, 4, 8, 7},
   { 8, 6, 2, 7, 15, 11, 0, 13, 14, 12, 5, 9, 3, 1, 4, 10},
   },
 
   {
   { 8, 6, 2, 7, 15, 11, 0, 13, 14, 12, 5, 9, 3, 1, 4, 10},
   { 9, 15, 6, 5, 7, 13, 0, 8, 14, 11, 10, 3, 12, 1, 2, 4},
   { 5, 14, 2, 6, 12, 15, 11, 4, 9, 1, 3, 10, 8, 7, 0, 13},
   { 3, 9, 0, 7, 1, 12, 6, 4, 13, 8, 10, 11, 2, 14, 5, 15},
   },
};
 
const int Pbox[32] = {
22, 8, 18, 5, 24, 14, 15, 7, 10, 27, 13, 32, 31, 11, 16, 20, 21, 3, 17, 
28, 1, 29, 9, 23, 25, 12, 6, 30, 4, 19, 2, 26
};

void addbit(uint64_t *block, uint64_t from,
            int position_from, int position_to)
{
    if(((from << (position_from)) & FIRSTBIT) != 0)
        *block += (FIRSTBIT >> position_to);
}

void Permutation(uint64_t* data, bool initial)
{
    uint64_t data_temp = 0;
    for(int ii = 0; ii < 64; ii++)
    {
        if(initial)
            addbit(&data_temp, *data, InitialPermutation[ii] - 1, ii);
        else
            addbit(&data_temp, *data, FinalPermutation[ii] - 1, ii);
    }
    *data = data_temp;
}
void rounds(uint64_t *data, uint64_t key)
{ 
    uint64_t right_block = 0;
    uint64_t right_block_temp = 0;
    FILE *input, *output;  
    // 1. Block expansion
    for(int ii = 0; ii < 48; ii++)
        addbit(&right_block, *data, (DesExpansion[ii] + 31), ii);
  
    // 2. Xor with the key
    right_block = right_block ^ key;

    // 3. Substitution
    int coordx, coordy;
    uint64_t substitued;

    for(int ii = 0; ii < 8; ii++)
    {
        coordx = ((right_block << 6 * ii) & FIRSTBIT) == FIRSTBIT ? 2 : 0;
        if( ((right_block << (6 * ii + 5)) & FIRSTBIT) == FIRSTBIT)
            coordx++;

        coordy = 0;
        for(int jj = 1; jj < 5; jj++)
        {
            if( ((right_block << (6 * ii + jj)) & FIRSTBIT) == FIRSTBIT)
            {
                coordy += 2^(4 - jj);
            }
        }
    
        substitued = DesSbox[ii][coordx][coordy];
        substitued = substitued << (60 - (4 * ii));
        right_block_temp += substitued;
    }
  
    // Right_block done
    right_block = right_block_temp;

    // 4. Permutation
    right_block_temp = 0;
  
    for(int ii = 0; ii < 32; ii++)
        addbit(&right_block_temp, right_block, Pbox[ii] - 1, ii);
  
    right_block = right_block_temp;

    // 5. Xor with the left block
    right_block = right_block ^ *data;
  
    // Combine the new block and the right block
    *data = (*data << 32) + (right_block >> 32);
}


int main(int argc, char ** argv)
{
    // Vars
    uint64_t key = 83247388437587L;
    uint64_t ivec = 183247389437587L;
    uint64_t k2 = 983247389437587L;
    int sz = 0;
    char buf[8];
    FILE * input = NULL;
    FILE * output = NULL;

    if (argc != 1)
    {
        fprintf(stderr, "Error:  wrong number of parameters\n");
        exit(-1);
    }

    input = stdin;
    output = stdout;

    size_t amount; // Used for fwrite
    uint64_t data;

    while((amount = fread(buf, 1, 8, input)) > 0)
    {
        int ix;
        ix = amount;
        sz += amount;
        while (ix < 8){
            buf[ix] = (amount == ix ? 0x10 : 0x20);
            ix++;
        }
        memcpy(&data, buf, 8);
        data ^= ivec;
        // Initial permutation
        Permutation(&data, 1);

        kx[11] ^= ivec;        
        for(int ii = 11; ii < 16; ii++)
            rounds(&data, kx[ii]);

        // Final permutation
        Permutation(&data, 0);
        ivec = data;
        // Write output
        fwrite(&data, 1, 8, output);
        data = 0;
    }
    fprintf(stderr,"Length of file %d\n", sz);
    if (sz % 8 == 0){
       buf[0] = 0x10;
       buf[1] = buf[2] = buf[3] = buf[4] = buf[5] = buf[6] = buf[7] = 0x20;
       memcpy(&data, buf, 8);
       data ^= ivec;
       kx[11] ^= ivec;        
       Permutation(&data, 1);
       for(int ii = 11; ii < 16; ii++)
           rounds(&data, kx[ii]);
       Permutation(&data, 0);
       fwrite(&data, 1, 8, output);
    }
//  fclose(input);
    fclose(output);

    return 0;
}                                 