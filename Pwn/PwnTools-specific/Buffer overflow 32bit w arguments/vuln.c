#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>

#define BUFSIZE 100
#define FLAGSIZE 64

/*

I need to write to the stack and print it, so I know 
what the return pointer address is, how much to reach it,
and then how the stack will look like when pushing the
arguments.

get the address of the return pointer



gdb ./vuln
r
CYCLIC-STRING = segfault
info frame
i r $eip -> 0x62616164

now we know the return address was over-written with 0x62616164, we need to see where this in our cyclic string
cyclic -l 0x62616164 = 112

*/

void win(unsigned int arg1, unsigned int arg2) {
  char buf[FLAGSIZE];
  FILE *f = fopen("flag.txt","r");
  if (f == NULL) {
    printf("%s %s", "Please create 'flag.txt' in this directory with your",
                    "own debugging flag.\n");
    exit(0);
  }

  fgets(buf,FLAGSIZE,f);
  if (arg1 != 0xCAFEF00D)
    return;
  if (arg2 != 0xF00DF00D)
    return;
  printf(buf);
}

void vuln(){
  char buf[BUFSIZE];
  gets(buf);
  puts(buf);
}

int main(int argc, char **argv){


  // sets buffering to zero, so if there is a seg fault the data (flag) will still be printed.
  setvbuf(stdout, NULL, _IONBF, 0);
  
  // sets the permissions of the current binary to the user ID running it (probably unprivileged user)
  gid_t gid = getegid();
  setresgid(gid, gid, gid);

  puts("Please enter your string: ");
  vuln();
  return 0;
}

