// EXPECT: 6, 13
#include <assert.h>
#include <stdlib.h>

int *late_if(int n) {
    int *a = malloc(n * sizeof(int));
    a[0] = n;
    if (a == NULL) return NULL;
    return a;
}

int *late_assert(int n) {
    int *d = malloc(sizeof(int));
    *d = n;
    assert(d != NULL);
    return d;
}
