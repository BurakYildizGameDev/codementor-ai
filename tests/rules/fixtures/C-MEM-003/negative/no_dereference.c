#include <stdlib.h>

void *xmalloc(size_t n) {
    void *p = malloc(n);
    return p;
}

void *xcalloc(size_t n) {
    return calloc(n, 1);
}

int size_of_node(void) {
    int *q = malloc(sizeof *q);
    int s = (int)sizeof *q;
    free(q);
    return s;
}
