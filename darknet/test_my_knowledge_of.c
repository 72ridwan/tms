#include <stdio.h>
#include <unistd.h> 

int main( int argc, char *argv[] )  {

   if( argc == 5 ) {
      printf("So you want to: %s objects in image file: %s\n", argv[1], argv[4]);
      printf("The configuration file you want to use is in %s\n", argv[2]);
      printf("and the weight is in file: %s\n", argv[3]);
      printf("Now, wait 3 seconds!\n");
      
      for (int i = 0; i < 3; i ++) {
          sleep(1);
          if (i == 0) {
              printf("One... ");
          } else if (i == 1) {
              printf("two... ");
          } else if (i == 2) {
              printf("three...\n");
          }
          fflush(stdout);
      }
      printf("Now you may go.");
   }
   else if( argc > 5 ) {
      printf("Too many arguments supplied.\n");
   }
   else {
      printf("One argument expected.\n");
   }
}