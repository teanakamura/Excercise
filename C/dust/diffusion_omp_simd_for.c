#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <immintrin.h>

#define NX 8192
#define NY 8192

float data[2][NY][NX];

/* in microseconds (us) */
double get_elapsed_time(struct timeval *begin, struct timeval *end)
{
    return (end->tv_sec - begin->tv_sec) * 1000000
            + (end->tv_usec - begin->tv_usec);
}

void init()
{
  int x, y;
  int cx = NX/2, cy = 0; /* center of ink */
  int rad = (NX+NY)/8; /* radius of ink */

  # pragma omp parallel for private(x)
  for(y = 0; y < NY; y++) {
    for(x = 0; x < NX; x++) {
      float v = 0.0;
      if (((x-cx)*(x-cx)+(y-cy)*(y-cy)) < rad*rad) {
	v = 1.0;
      }
      data[0][y][x] = v;
      data[1][y][x] = v;
    }
  }
  return;
}

void simd_calc(int x, int y, int from, int to) {
  int i;
  float temp1[8], temp2[8], temp3[8], temp4[8], temp5[8];
  for (i = 0; i < 8; i++) {
    temp1[i] = data[from][y][x+i];
    temp2[i] = data[from][y][x+i-1];
    temp3[i] = data[from][y][x+i+1];
    temp4[i] = data[from][y-1][x+i];
    temp5[i] = data[from][y+1][x+i];
  }
  register __m256 reg1 = _mm256_load_ps(temp1);
  register __m256 reg2 = _mm256_load_ps(temp2);
  reg1 = _mm256_add_ps(reg1, reg2);
  reg2 = _mm256_load_ps(temp3);
  reg1 = _mm256_add_ps(reg1, reg2);
  reg2 = _mm256_load_ps(temp4);
  reg1 = _mm256_add_ps(reg1, reg2);
  reg2 = _mm256_load_ps(temp5);
  reg1 = _mm256_add_ps(reg1, reg2);
  __m256 multi_vector = _mm256_set1_ps(0.2);
  reg1 = _mm256_mul_ps(reg1, multi_vector);

  _mm256_storeu_ps(&data[to][y][x], reg1);
}

/* Calculate for one time step */
/* Input: data[t%2], Output: data[(t+1)%2] */
void calc(int nt)
{
  int t, x, y;

  for (t = 0; t < nt; t++) {
    int from = t%2;
    int to = (t+1)%2;

#if 1
    printf("step %d\n", t);
    fflush(0);
#endif

    # pragma omp parallel for private(x)
    for (y = 1; y < NY-1; y++) {
      for (x = 1; x < NX-1; x += 8) {
        simd_calc(x, y, from, to);
      }
    }
  }

  return;
}

int main(int argc, char *argv[])
{
  struct timeval t1, t2;
  int nt = 20; /* number of time steps */

  if (argc >= 2) { /* if an argument is specified */
      nt = atoi(argv[1]);
  }

  init();

  gettimeofday(&t1, NULL);

  calc(nt);

  gettimeofday(&t2, NULL);

  {
      double us;
      double gflops;
      int op_per_point = 5; // 4 add & 1 multiply per point

      us = get_elapsed_time(&t1, &t2);
      printf("Elapsed time: %.3lf sec\n", us/1000000.0);
      gflops = ((double)NX*NY*nt*op_per_point)/us/1000.0;
      printf("Speed: %.3lf GFlops\n", gflops);
      printf("Result: %.3lf\n", data[(nt-1)%2][1][NX/4]);
  }

  return 0;
}
