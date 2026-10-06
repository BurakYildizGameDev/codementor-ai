#include <stdlib.h>

int *early_return(int n) {
    int *a = malloc(n * sizeof(int));
    if (!a) {
        return NULL;
    }
    a[0] = n;
    return a;
}

int first_or_zero(int n) {
    int *b = calloc(n, sizeof(int));
    int r = (b != NULL && b[0] == 0) ? 1 : 0;
    free(b);
    return r;
}

int ternary(void) {
    int *c = malloc(sizeof(int));
    return c ? (*c = 1) : 0;
}

int nested_block(int n) {
    int *d = malloc(n * sizeof(int));
    {
        if (d == NULL) goto fail;
        d[0] = n;
    }
    free(d);
    return 0;
fail:
    return -1;
}

int *loop_guard(int n) {
    int *e = malloc(n * sizeof(int));
    while (e == NULL) e = malloc(n * sizeof(int));
    e[0] = n;
    return e;
}
