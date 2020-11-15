#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#include <errno.h>

int main()
{
	int fd = open("doc.txt", O_WRONLY | O_CREAT);
	char buf[] = "Hello World!";

	if(fd == -1)
	{
		printf("Error number %d \n", errno);
		perror("Open!");
	}
	write(fd, buf, strlen(buf));

	if(close(fd) != 0)
	{
		perror("Closing file!");
		exit(1);
	}

	return 0;
}
