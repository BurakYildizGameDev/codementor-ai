#include <assert.h>
#include <stdlib.h>

int *a1(int n) {
    int *a = malloc(n * sizeof(int));
    if (a == NULL) return NULL;
    a[0] = n;
    return a;
}

int *a2(int n) {
    int *b = calloc(n, sizeof(int));
    if (!b) return NULL;
    b[0] = n;
    return b;
}

int *a3(int n) {
    int *c;
    if ((c = malloc(sizeof *c * n)) == NULL) return NULL;
    c[0] = n;
    return c;
}

int *a4(int n) {
    int *d = malloc(sizeof(int));
    assert(d);
    *d = n;
    return d;
}

int *a5(int n) {
    int *e = malloc(sizeof(int));
    if (e) {
        *e = n;
    }
    return e;
}
