#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/mman.h>
#include <sys/sysmacros.h>
#include <pthread.h>
#include <semaphore.h>

#define NTHRS 5
typedef struct pthr{
	pthread_t thread;
	int identifier;
};

/* this data is shared among the thread */
int count = 0;

sem_t sem;
pthread_mutex_t mtx;

int barrier_point();
void* tfun(void* );

int main(void)
{
	int error;

	if(sem_init(&sem, 0, 0)){
		perror(NULL);
		return errno;
	}

	if((error = pthread_mutex_init(&mtx, NULL)) != 0){
		perror(NULL);
		return error;
	}

	struct pthr *thr = (struct pthr*)malloc((NTHRS + 1) * sizeof(struct pthr));
	if(thr == NULL)
	{
		fprintf(stderr, "Memory allocation failure!");
		exit(EXIT_FAILURE);
	}

	for(int i = 0; i < NTHRS; i++)
	{
		thr[i].identifier = i;
		if((error = pthread_create(&thr[i].thread, NULL, tfun, &thr[i].identifier)) != 0){
			perror("Unable to create thread");
			return error;
		}
		sleep(1);
	}

	for(int i = 0; i < NTHRS; i++)
	{
		if((error = pthread_join(thr[i].thread, NULL)) != 0){
			perror("Unable to join thread");
			return error;
		}
	}

	if((error = pthread_mutex_destroy(&mtx)) != 0)
	{
		perror(NULL);
		return error;
	}

	if(sem_destroy(&sem))
	{
		perror("Unable to destrooy the semaphore!");
		return error;
	}

	exit(EXIT_SUCCESS);
}

int barrier_point()
{
	pthread_mutex_lock(&mtx);
	count++;
	pthread_mutex_unlock(&mtx);

	if(count < NTHRS){
		if(sem_wait(&sem)){
			perror(NULL);
			return errno;
		}
	}
	else{
		for(int i = 0; i < NTHRS - 1; i++){
			if(sem_post(&sem)){
				perror(NULL);
				return errno;
			}
			sleep(1);
		}
	}
	return 0;
}


void* tfun(void* arg)
{
	int tid = *(int*)arg;
	printf("%d reached the barrier\n", tid);
	barrier_point();
	printf("%d passed the barrier\n", tid);

	return NULL;
}
