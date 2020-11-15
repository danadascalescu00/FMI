#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <unistd.h>
#include <errno.h>
#include <sys/sysmacros.h>


char *str_result; /* this data is shared by the thread */
void *strrev(void *arg); /* thread call in this function */

int main(int argc, char* argv[])
{
	pthread_t thr; //thread identifier
	pthread_attr_t attr; //set of thread attributes

	if(argc < 2 || argc > 3)
	{
		fprintf(stderr, "Only one argument must be passed!");
		exit(1);
	}

	/* get the default attributes */
	pthread_attr_init(&attr);
	/* create the thread */
	if(pthread_create(&thr, &attr, strrev, argv[1]))
	{
		perror(NULL);
		return errno;
	}
	/*wait for the thread to exit */
	if(pthread_join(thr, &str_result))
	{
		perror(NULL);
		return errno;
	}

	printf("%s\n", (char*)str_result);

	return 0;

}

void *strrev(void *arg)
{
	char *str_in = (char*)arg;
	char *reverse_string = (char*)malloc(strlen(str_in) * sizeof(char));
	if(reverse_string == NULL)
	{
		fprintf(stderr, "Memory allocation failure!");
		exit(EXIT_FAILURE);
	}

	for(int i = 0; i < strlen(str_in); i++)
		reverse_string[i] = str_in[strlen(str_in) - i - 1];

	return reverse_string;
}
