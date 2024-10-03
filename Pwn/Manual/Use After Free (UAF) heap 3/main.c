#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*

HEAP Buffer Overflow + UAF (User After Free) exploitation
to get arbitrary variable manipulation to get the flag.


1) free x
2) allocate 30 (smaller than 35 otherwise it won't overlap in the memory region)
3) AAAAAAAAAAAAAAAAAAAAAAAAAAAAAApico
4) print flag
5) get flag

only reason our payload overflows is bcs we're using unsecure scanf() function without
any restrictions

how the HEAP looks (kind of)

x
    a (10)
    b (10)
    c (10)
    flag (5)
attacker_allocated_data (will overlap with x, bcs our size is 30 so it's smaller and it'll choose the next free region
                        which ic where "x" was)

then, with scanf we write 30 A to fill up attacker_allocated_data (over-writes a, b, and c) then we 
type "pico" to overwrite "flag"

picoCTF{now_thats_free_real_estate_e8938a97}

*/



typedef struct {
  char a[10];
  char b[10];
  char c[10];
  char flag[5];
} object;

int num_allocs;
object *x;


int main(){
    printf("%lu\n", sizeof(object));
    x = malloc(sizeof(object));

    strncpy(x->flag, "bico", 5);

    free(x);

    char* attacker_controller = malloc(30);



    printf("Data for flag: ");
    fflush(stdout);
    scanf("%s", attacker_controller);



    printf("x address: %p\nattacker_controlled address: %p\n", x, attacker_controller);
    printf("x->flag's address: %p\n", x->flag);
    printf("Flag's contents: %s\n", x->flag);



    return 0;
}