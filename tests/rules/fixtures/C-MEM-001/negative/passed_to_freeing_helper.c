#include <stdlib.h>

void destroy(int *values) {
    free(values);
}

void run(int n) {
    int *values = malloc(n * sizeof *values);
    if (values == NULL) return;
    values[0] = n;
    destroy(values);
}
