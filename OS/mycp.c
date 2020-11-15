#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <fcntl.h>
#include <errno.h>

int main(int argc, char *argv[])
{
	char buffer[1024];
	int source_file, destination_file;
	struct stat sb;
	ssize_t bytes;

	if(argc != 3)
	{
		printf("Must be passed only two arguments!");
		perror("Arguments list!");
		exit(EXIT_FAILURE);
	}

	source_file = open(argv[1], O_RDONLY);
	if(source_file == -1)
	{
		printf("Error! Couldn't find the file for reading!");
		exit(1);
	}

	if(stat(argv[1], &sb) == -1)
	{
		perror("Source file!");
		return errno;
	}
	printf("Source file (%s) takes %ld bytes on the disk\n", argv[1], sb.st_size);


	destination_file = open(argv[2], O_WRONLY | O_CREAT, S_IRWXU, S_IROTH);
	if(destination_file == -1)
	{
		printf("Error! Couldn't create or open the ddestination file!");
		exit(1);
	}

	if(stat(argv[2], &sb) == -1)
	{
		perror("Destination file!");
		return errno;
	}


	while((bytes = read(source_file, buffer, sizeof(buffer)))!=0)
		write(destination_file, buffer, bytes);

	if(close(destination_file) != 0)
	{
		printf("Error!");
		exit(1);
	}

	return 0;
}
