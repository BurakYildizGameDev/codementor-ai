#include <stdlib.h>

int *make_zeroes(int n) {
    int *a = malloc(n * sizeof(int));
    if (a == NULL) return NULL;
    for (int i = 0; i < n; i++) a[i] = 0;
    return a;
}
