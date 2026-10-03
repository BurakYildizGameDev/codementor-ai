#include <stdio.h>
#include <stdlib.h>

int process_data(int n) {
    int *buffer = (int *)malloc(n * sizeof(int));
    if (buffer == NULL) {
        return -1;
    }
    for (int i = 0; i < n; i++) {
        buffer[i] = i * 2;
    }
    int sum = 0;
    for (int i = 0; i < n; i++) {
        sum += buffer[i];
    }
    return sum;
}
