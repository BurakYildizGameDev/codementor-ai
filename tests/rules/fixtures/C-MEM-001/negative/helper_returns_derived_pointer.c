#include <stdlib.h>

int *pick(int *values, int i) {
    return values + i;
}

int first(int n) {
    int *values = malloc(n * sizeof *values);
    if (values == NULL) return 0;
    values[0] = n;
    return *pick(values, 0);
}
