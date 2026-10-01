#include <stdio.h>
#include <stdlib.h>

static void die_if_null(void *p) {
    if (p == NULL) {
        fprintf(stderr, "bellek yok\n");
        exit(1);
    }
}

int *make_v(int n) {
    int *v = malloc(n * sizeof(int));
    die_if_null(v);
    v[0] = n;
    return v;
}

int *make_w(int n) {
    int *w = malloc(n * sizeof(int));
    if (w == (void *)0) return NULL;
    w[0] = n;
    return w;
}
