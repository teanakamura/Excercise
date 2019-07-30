#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

#define CACHE_SIZE 35840000

int nx = 8192;
int ny = 8192;
float *data;
int x_block_size;

/* in microseconds (us) */
double get_elapsed_time(struct timeval *begin, struct timeval *end)
{
    return (end->tv_sec - begin->tv_sec) * 1000000
            + (end->tv_usec - begin->tv_usec);
}

void init()
{
  int x, y;
  int cx = nx/2, cy = 0; /* center of ink */
  int rad = (nx+ny)/8; /* radius of ink */

  # pragma omp parallel for private(x)
  for(y = 0; y < ny; y++) {
    for(x = 0; x < nx; x++) {
      float v = 0.0;
      if (((x-cx)*(x-cx)+(y-cy)*(y-cy)) < rad*rad) {
	v = 1.0;
      }
      data[y * (2 * nx) + x * 2] = v;
      data[y * (2 * nx) + x * 2 + 1] = v;
    }
  }
  return;
}

/* Calculate for one time step */
/* Input: data[t%2], Output: data[(t+1)%2] */
void calc(int nt)
{
  int t, x, y, bx;

  for (t = 0; t < nt; t++) {
    int from = t%2;
    int to = (t+1)%2;

#if 1
    printf("step %d\n", t);
    fflush(0);
#endif

    # pragma omp parallel for private(x, bx)
    for (y = 1; y < ny-1; y++) {
      for (bx = 1; bx < nx-1; bx += x_block_size) {
        for (x = bx; x < bx + x_block_size && x < nx-1; x++) {
  	       data[y * (2*nx) + x*2 + to] = 0.2 * (data[y * (2*nx) + x*2 + from]
              + data[y * (2*nx) + (x-1)*2 + from]
              + data[y * (2*nx) + (x+1)*2 + from]
              + data[(y-1) * (2*nx) + x*2 + from]
              + data[(y+1) * (2*nx) + x*2 + from]);
        }
      }
    }
  }

  return;
}

void calc_block_size()
{
  x_block_size = CACHE_SIZE / (sizeof(float) * ny * 2);
  printf("x_block_size: %d\n", x_block_size);
}

int main(int argc, char *argv[])
{
  struct timeval t1, t2;
  int nt = 20; /* number of time steps */

  if (argc >= 2) { /* if an argument is specified */
      nt = atoi(argv[1]);
  }
  if (argc >= 4) {
      nx = atoi(argv[2]);
      ny = atoi(argv[3]);
  }
  printf("nx: %d, ny: %d\n", nx, ny);

  data = (float *)malloc(sizeof(float) * 2 * nx * ny);

  init();
  calc_block_size();

  gettimeofday(&t1, NULL);

  calc(nt);

  gettimeofday(&t2, NULL);

  {
      double us;
      double gflops;
      int op_per_point = 5; // 4 add & 1 multiply per point

      us = get_elapsed_time(&t1, &t2);
      printf("Elapsed time: %.3lf sec\n", us/1000000.0);
      gflops = ((double)nx*ny*nt*op_per_point)/us/1000.0;
      printf("Speed: %.3lf GFlops\n", gflops);
      printf("Result: %.3lf\n", data[nx*2 + (nx/4)*2 + (nt-1)%2]);
  }

  return 0;
}
