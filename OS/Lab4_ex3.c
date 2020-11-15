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
	int wstatus;
	pid_t pidc, pid;

	if(argc < 2)
	{
		perror("At least one element must be passed as argument!");
		return -1;
	}

	for(int i = 1; i < argc; i++)
	{
		int n = atoi(argv[i]);

		pid = fork();
		if(pid < 0)
			return errno;
		if(pid == 0)
		{
			printf("%d: ", n);
			while(n != 1)
			{
				printf("%d ", n);
				if(n % 2 == 0)
					n = n / 2;
				else
					n = 3 * n + 1;
			}
			if(n == 1){
				printf("%d\n", n);
				exit(EXIT_SUCCESS);
			}
			else
				exit(EXIT_FAILURE);
		}
		else{
			do{
				pidc = waitpid(pid, &wstatus, WUNTRACED | WCONTINUED);

				if( pidc == -1){
					perror("waitpid");
					return -1;
				}

				if(WIFEXITED(wstatus)){
					printf("exited, status = %d\n", WEXITSTATUS(wstatus));
				}else if(WIFSIGNALED(wstatus)){
					printf("kill by the signal: %d\n", WTERMSIG(wstatus));
				}else if(WIFSTOPPED(wstatus)){
					printf("stopped by signal %d\n", WSTOPSIG(wstatus));
				}else if(WIFCONTINUED(wstatus)){
					printf("continued\n");
				}

			}while(!WIFEXITED(wstatus) && !WIFSIGNALED(wstatus));

			printf("Done Parent: %d, Me: %d\n\n", getpid(), pidc);
		}
	}

	return 0;
}

