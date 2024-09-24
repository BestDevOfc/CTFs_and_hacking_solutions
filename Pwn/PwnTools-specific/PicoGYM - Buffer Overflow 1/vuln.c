#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include "asm.h"

#define BUFSIZE 32
#define FLAGSIZE 64

// we need to overwrite the return address from get_return_address() to win(),
// so we need to figure out the address of this function.
void win() {
  char buf[FLAGSIZE];
  FILE *f = fopen("flag.txt","r");

  fgets(buf,FLAGSIZE,f);
  printf(buf);
}

void vuln(){
  char buf[BUFSIZE];
  gets(buf);
  
  printf("Okay, time to return... Fingers Crossed... Jumping to 0x%x\n", get_return_address());
}

int main(int argc, char **argv){

  // this is just setup stuff, so if someone pops a shell,
  // you won't be root
  // there's no buffering, IF you pop a shell, it'll still print all the output.
  setvbuf(stdout, NULL, _IONBF, 0);
  
  // current ID is being grabbed, someone prolly ran this NOT as root.
  gid_t gid = getegid();
  setresgid(gid, gid, gid);

  // vulnerable function:
  puts("Please enter your string: ");
  vuln();
  /* this is where it'll jump back */

  return 0;
}

