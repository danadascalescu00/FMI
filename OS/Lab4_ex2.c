#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <errno.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/wait.h>

int main(int argc,char *argv[])
{

	if(argc != 2)
	{
		perror("Only one argumen must be passed!");
		exit(EXIT_FAILURE);
	}

	int n = atoi(argv[1]);

	pid_t pid = fork();
	if(pid < 0)
		return errno;
	if(pid == 0)
	{
		printf("%d: ", n);
		while( n!=1)
		{
			printf("%d ", n);
			if(n % 2 == 0)
				n = n /2;
			else
				n = 3*n + 1;
		}
		if(n == 1)
			printf("%d\n", n);
	}
	else{
		int status;
		pid = waitpid(-1, &status, 0);
		printf("Child %d finished\n", pid);
	}

	return 0;
}

