#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <pthread.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/sysmacros.h>

#define MAX_RESOURCES 24
int available_resources = MAX_RESOURCES;
pthread_mutex_t mtx;

int increase_count(int );
int decrease_count(int );
void* job(void* );

int main(void)
{
	if(pthread_mutex_init(&mtx, NULL))
	{
		perror(NULL);
		return errno;
	}

	int count;
	pthread_t* thr = (pthread_t*)malloc((MAX_RESOURCES + 1) * sizeof(pthread_t));
	if(thr == NULL)
	{
		fprintf(stderr, "Memory allocation failure!");
		exit(EXIT_FAILURE);
	}

	for(int i = 0; i < MAX_RESOURCES; i++)
	{
		int error;
		count = rand() % (available_resources + 1);
		if((error = pthread_create(&thr[i], NULL, job, count))!=0)
		{
			perror("Unable to create thread");
			return error;
		}
	}

	for(int i = 0; i < MAX_RESOURCES; i++)
	{
		int error;
		if((error = pthread_join(thr[i], NULL))!=0)
		{
			perror("thread join");
			return error;
		}

	}
	pthread_mutex_destroy(&mtx);

	exit(EXIT_SUCCESS);
}

int decrease_count(int count)
{
	pthread_mutex_trylock(&mtx);
	if(available_resources < count)
	{
		pthread_mutex_unlock(&mtx);
		return -1;
	}
	else{	available_resources = available_resources - count;
		printf("Got %d resources %d remaining\n", count, available_resources);
	}
	pthread_mutex_unlock(&mtx);

	return 0;
}

int increase_count(int count)
{
	pthread_mutex_lock(&mtx);
	available_resources = available_resources + count;
	printf("Released %d resources %d remaining\n", count, available_resources);
	pthread_mutex_unlock(&mtx);
}

void* job(void* arg)
{
	int count = (int)arg;

	while(decrease_count(count) == -1);
	increase_count(count);

	return NULL;
}
