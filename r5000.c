/********************
https://www.includehelp.com/c-programs/c-program-to-print-contents-in-reverse-order-of-a-file-like-tac-command-in-linux.aspx?fbclid=IwAR2XeFJE8LtT5QF9-wS4BX6kyUZuG4ooARWyvhAZNC3yuVzCByyJBRSQP4Q
Home » C solved programs
 » C file handling programs

C program to print contents in reverse order of a file (just like TAC command in Linux)
This program will print the contents of given file name in reverse order. Just like tac command in Linux. tac command displays contents of the file in reverse order. Same as tac command in this program you have to supply file name.
The syntax of executing this program
./program-name file-name

*/
//Write a program to print reverse content of file
#include <stdio.h>
#include <string.h>
 
int main(int argc, char *argv[])
{
    FILE *fp1;
    char buf [5000]; 
    int c, cnt = 0;
    int i = 0;
     
    if( argc != 1 )
    {
        printf("Wrong number of arguments!!!\n");
        printf("Please use \"program\" without command line parameters\n");
        return -1;
    }
     
    fp1 = stdin;
    if( fp1 == NULL )
    {
        printf("\n%s Stdin can not be used : \n");
        return -1;
    }
     
    cnt = 0; 
    while( (c = fgetc(fp1)) != -1 )
    {
        buf[cnt++] = c;
        if (cnt == sizeof(buf)){
           while (cnt > 0){
              cnt--;
              fputc(buf[cnt], stdout);
           }
        }
    }
    while (cnt > 0){
       cnt--;
       fputc(buf[cnt], stdout);
    }

    fprintf(stderr,"Finished\n");
}
     