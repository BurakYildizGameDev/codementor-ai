// EXPECT: 5
#include <stdlib.h>

int sum_first(int n) {
    int *values = malloc(n * sizeof *values);
    if (values == NULL) return 0;
    values[0] = n;
    return total(values, n);
}

int total(const int *values, int n) {
    int s = 0;
    for (int i = 0; i < n; i++) s += values[i];
    return s;
}
