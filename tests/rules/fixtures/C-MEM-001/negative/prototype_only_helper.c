#include <stdlib.h>

int checksum(const int *values, int n);

int report(int n) {
    int *values = malloc(n * sizeof *values);
    if (values == NULL) return 0;
    values[0] = n;
    return checksum(values, n);
}
