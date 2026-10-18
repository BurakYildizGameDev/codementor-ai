#include <stdlib.h>

#ifdef NO_ALIGN
static int checksum(const int *values, int n) {
    int s = 0;
    for (int i = 0; i < n; i++) s += values[i];
    return s;
}
#else
static int checksum(const int *values, int n) {
    return values[0] * n;
}
#endif

int report(int n) {
    int *values = malloc(n * sizeof *values);
    if (values == NULL) return 0;
    values[0] = n;
    return checksum(values, n);
}
