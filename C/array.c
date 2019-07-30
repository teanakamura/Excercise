#include <stdio.h>

int main() {
  float arr[2][2][2];
  printf("000: %p\n", &arr[0][0][0]);
  printf("001: %p\n", &arr[0][0][1]);
  printf("010: %p\n", &arr[0][1][0]);
  printf("011: %p\n", &arr[0][1][1]);
  printf("100: %p\n", &arr[1][0][0]);
  printf("101: %p\n", &arr[1][0][1]);
  printf("110: %p\n", &arr[1][1][0]);
  printf("111: %p\n", &arr[1][1][1]);

  printf("%lu\n", sizeof(float));
  printf("%lu\n", sizeof(float) + 2);
}
