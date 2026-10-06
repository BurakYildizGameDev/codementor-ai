// EXPECT: 6
#include <stdlib.h>

int *pair(int n) {
    int *b = malloc(sizeof(int));
    int *a = malloc(n * sizeof(int));
    if (b == NULL) return NULL;
    a[0] = n;
    *b = n;
    free(b);
    return a;
}
