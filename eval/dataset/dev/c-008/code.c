#include <stdlib.h>

int average(const int *values, int n) {
    int *tmp = malloc(n * sizeof(int));
    int total = 0;
    for (int i = 0; i < n; i++) {
        tmp[i] = values[i] * 2;
        total += tmp[i];
    }
    return total / (2 * n);
}
