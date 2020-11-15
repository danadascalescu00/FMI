
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/mman.h>
#include <sys/sysmacros.h>

int main(int argc, char *argv[])
{
	fprintf(stdout, "Starting parent %d\n", getpid());

	int wstatus, shm_fd;
	char shm_name[] = "collatz";
	struct stat sb;
	pid_t pid;
	unsigned int displacement = 0,  offset = 0;
	size_t shm_size = getpagesize() * (argc - 1);

	if(argc < 2)
	{
		fprintf(stderr, "At least one argument must be passed!");
		exit(EXIT_FAILURE);
	}

	int *pid_children = (int*)malloc((argc - 1) * sizeof(int));
	if(pid_children == NULL)
	{
		fprintf(stderr, "Memory not allocated!");
		exit(1);
	}

	/* Create shared memory object */
	shm_fd = shm_open(shm_name, O_CREAT | O_RDWR, S_IRUSR | S_IWUSR);
	if(shm_fd < 0)
	{
		perror(NULL);
		return errno;
	}

	/* Define size */
	if(ftruncate(shm_fd, shm_size) == -1) {
		perror(NULL);
		shm_unlink(shm_name);
		return errno;
	}

	for(int i = 1; i < argc; i ++)
	{
		int n = atoi(argv[i]), aux = atoi(argv[i]);
		if(n < 0)
		{
			fprintf(stderr, "Only positive numbers!\n");
			i = i + 1;
		}

		pid_children[i - 1] = fork();
		if(pid_children[i - 1] < 0)
			return errno;
		if(pid_children[i - 1] == 0)
		{
			/* Child instructions */
			char *shm_ptr_child = mmap(0, getpagesize(), PROT_READ | PROT_WRITE, MAP_SHARED, shm_fd, (i - 1) * getpagesize());
			if(shm_ptr_child == MAP_FAILED)
			{
				perror(NULL);
				shm_unlink(shm_name);
				return errno;
			}

			int count = 0;
			int *series = (int*)malloc(count * sizeof(int));
			if(series == NULL)
			{
				fprintf(stderr, "Memory allocation error!");
				exit(1);
			}

			*(series + count) = n;
			while(n != 1)
			{
				count = count + 1;
				series = (int*)realloc(series, (count + 1) * sizeof(int));
				if(series ==  NULL)
				{
					fprintf(stderr, "Memory allocation failure!");
					free(series);
					exit(EXIT_FAILURE);
				}

				if(n % 2== 0)
					n = n / 2;
				else
					n = 3 * n + 1;

				*(series + count) = n;
			}
			if(n == 1){
				offset = sprintf(shm_ptr_child, "%d : ", aux);
				shm_ptr_child += offset;
				for(int i = 0; i < count + 1; i++)
				{
					offset = sprintf(shm_ptr_child, "%d ", series[i]);
					shm_ptr_child += offset;
				}

				free(series);
				munmap(shm_ptr_child, getpagesize());

				fprintf(stdout, "Done Parent: %d, Me: %d \n", getppid(), getpid());
				exit(EXIT_SUCCESS);
			}
			else
				exit(EXIT_FAILURE);
		}
		else{
			/* Parent instructions */
			do{
				pid = waitpid(pid_children[i - 1], &wstatus, WUNTRACED | WCONTINUED);
				if(pid == -1)
				{
					perror("waitpid");
					return -1;
				}

				if(WIFEXITED(wstatus)){
					fprintf(stdout, "exited, status = %d\n", WEXITSTATUS(wstatus));
				}else if(WIFSIGNALED(wstatus)) {
					fprintf(stdout, "killed by the signal: %d\n", WTERMSIG(wstatus));
				}else if(WIFSTOPPED(wstatus)) {
					fprintf(stdout, "stopped by the signal %d\n", WSTOPSIG(wstatus));
				}else if(WIFCONTINUED(wstatus)) {
					fprintf(stdout, "continued\n");
				}

			}while(!WIFEXITED(wstatus) && !WIFSIGNALED(wstatus));

		}
	}

	for(int i = 0; i < argc - 1; i++)
	{
		char *shm_ptr = mmap(0, getpagesize(), PROT_READ, MAP_SHARED, shm_fd, i * getpagesize());
		fprintf(stdout, "%s\n", shm_ptr);
		munmap(shm_ptr, getpagesize());
	}
	shm_unlink(shm_name);

	printf("\nDone Parent: %d, Children: %d \n", getppid(), getpid());

	return 0;
}
