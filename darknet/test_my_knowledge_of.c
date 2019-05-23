#include <stdio.h>

#include <unistd.h>

#include <signal.h>

#include <stdlib.h>

#include <limits.h>


// You can try to compile this code into something like this:
// gcc test_my_knowledge_of.c -o test_my_knowledge_of_c

int main(int argc, char * argv[]) {

  char cwd[PATH_MAX];

  // Print current working directory and PID

  if (getcwd(cwd, sizeof(cwd)) != NULL) {
    printf("Current working dir: %s\n", cwd);
    printf("pid this: %d\n", getpid());
  } else {
    perror("getcwd() error");
    return 1;
  }

  if (argc == 5) {

    // Get all the arguments supplied to this process

    printf("So you want to: %s objects in image file: %s\n", argv[1], argv[4]);
    printf("The configuration file you want to use is in %s\n", argv[2]);
    printf("and the weight is in file: %s\n", argv[3]);
    printf("Now, wait 3 seconds!\n");

    FILE * fp;
    char ch;
    char pid_main[30];
    int len = 0;
    int pid_main_int;

    // Read the main_pid file

    fp = fopen("main_pid", "r");

    if (fp == NULL) {
      perror("Oops! We can't open the main_pid.\n");
    } else {
      ch = fgetc(fp);
      while (ch != EOF) {
        pid_main[len] = ch;
        ch = fgetc(fp);
        len++;
      }
      pid_main[len] = '\0';

      printf("The Other PID: %s\n", pid_main);
      pid_main_int = atoi(pid_main);

      for (int i = 0; i < 2; i++) {
        sleep(1);
        if (i == 0) {
          printf("One... ");
        } else if (i == 1) {
          printf("two... ");
        } else if (i == 2) {
          printf("three...\n");
        } else {
          printf("..");
        }

        fflush(stdout);
      }
      
      // This is the expected behavior of image.c in the darknet.
      // It prints the boundaries in the hasil_prediksi.csv.
      // It should be copied to the frame folder.
          
      FILE *fpredict;
      fpredict = fopen("hasil_prediksi.csv", "w+");
      fprintf(fpredict, "object, probability, left, top, right, bottom\n");
      fclose(fpredict);
      
      // Send a SIGUSR1 signal to the PID
      // so that the detections can be saved by Python process.

      kill(pid_main_int, SIGUSR1);
      printf("We sent a signal to the PID! Check it out! Bye!");
    }
  } else {
    printf("Five arguments expected.\n");
  }
}