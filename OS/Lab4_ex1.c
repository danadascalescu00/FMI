#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/wait.h>

int main()
{
	pid_t pid = fork();
	if(pid < 0)
		return errno;
	if(pid == 0){
		/* Child's instructions */
		char *argv[] = {"ls", NULL};
		int error = execve("/bin/ls", argv, NULL);
		printf("Status exit : %d\n", error);
	}
	else{
		/* Parent's instructions */
		int returnStatus;
		pid_t pidc = waitpid(pid, &returnStatus, 0); /* Parent's process waits here for his child to terminate the process */
		printf("Parent: %d, Child: %d\n", getpid(), pidc);
		/* Verify if the child process terminates withouut error */
		if(returnStatus == 0)
			printf("Child process terminated normally\n");
		if(returnStatus == 1)
			printf("Child process terminated with an error");
	}

	return 0;
}
