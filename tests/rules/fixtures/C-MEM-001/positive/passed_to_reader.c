// EXPECT: 13
#include <stdlib.h>

int sum(const int *values, int n) {
    int total = 0;
    for (int i = 0; i < n; i++) {
        total += values[i];
    }
    return total;
}

int average(int n) {
    int *values = malloc(n * sizeof *values);
    if (values == NULL) return 0;
    for (int i = 0; i < n; i++) values[i] = i;
    return sum(values, n) / n;
}
