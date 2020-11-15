#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/sysmacros.h>
#include <pthread.h>

/* this data is shared by the thread */
unsigned int n, m, p, q;
int **A, **B;
int count = 0;

int **init_matrix(int , int);
void *multiplication(void *); /* thread call in this function */

int main(int argc, char *argv[])
{
	if(argc != 5)
	{
		fprintf(stderr, "Invalid arguments list!");
		return -1;
	}

	n = atoi(argv[1]);
	m = atoi(argv[2]);
	p = atoi(argv[3]);
	q = atoi(argv[4]);

	if(n < 0 || m < 0 || p < 0 || q < 0)
	{
		fprintf(stderr, "The arguments must be natural numbers!");
		return -1;
	}

	if(p != q)
	{
		fprintf(stderr, "Cannot perform the multiplication! (columns number of A != lines number of B)");
		exit(EXIT_FAILURE);
	}

	A = init_matrix(m, p);
	B = init_matrix(p, n);

	if(A == NULL || B == NULL)
	{
		fprintf(stderr, "Memory allocation failure!");
		return -1;
	}

	fprintf(stdout, "Matrix A: \n");
	for(int i = 0; i < m; i++)
	{
		for(int j = 0; j < p; j++)
			fprintf(stdout, "%d ", A[i][j]);
		fprintf(stdout, "\n");
	}

	fprintf(stdout, "\nMatrix B: \n");
	for(int i = 0; i < p; i++)
	{
		for(int j = 0; j < n; j ++)
			fprintf(stdout, "%d ", B[i][j]);
		fprintf(stdout, "\n");
	}

	pthread_t* threads = (pthread_t*)malloc((m*n)*sizeof(pthread_t));
	if(threads == NULL)
	{
		fprintf(stderr, "Memory allocation failure!");
		exit(EXIT_FAILURE);
	}

	//Creating a thread for a single element of the resultant matrix, each threads is evaluating its own part
	int *data = NULL;
	for(int i = 0; i < m; i++)
	{
		for(int j = 0; j < n; j++)
		{
			//storing the column of the first matrix and the line of the second one which will be passed as argument
			data = (int*)malloc((m + n + 1) * sizeof(int));
			data[0] = p;
			for(int k = 0; k < p; k++)
				data[k + 1] = A[i][k];

			for(int k = 0; k < p; k++)
				data[p + 1 + k] = B[k][j];

			if(pthread_create(&threads[count++], NULL, multiplication, (void*)(data)))
			{
				perror(NULL);
				return errno;
			}
		}
	}

	printf("\nOutput: resultant matrix: \n");
	for(int i = 0; i < m*n; i++)
	{
		void* collect;

		//Joinig all tthreads and collecting return value
		pthread_join(threads[i], &collect);

		printf("%d ", *(int *)collect);
		if((i + 1) % n == 0)
			printf("\n");
	}

	return 0;
}

int **init_matrix(int L, int C)
{
	int **matrix = (int**)malloc(L * sizeof(int*));
	for(int i = 0; i < L; i++)
		matrix[i] = (int*)calloc(C, sizeof(int));

	for(int i = 0; i <  L; i++)
	{
		for(int j = 0; j < C; j++)
		{
			matrix[i][j] = rand() % (L * C + 1);
		}
	}

	return matrix;
}

void *multiplication(void *arg)
{
	int *elements = (int*)arg;
	int ncolumn = elements[0]; // number of columns of the firts matrix = number of lines of the second matrix
	int sum = 0;

	for(int i = 1; i <= ncolumn; i++)
		sum += elements[i] * elements[i + ncolumn];

	int *result = (int*)malloc(sizeof(int));
	*result = sum;

	pthread_exit(result);
}
