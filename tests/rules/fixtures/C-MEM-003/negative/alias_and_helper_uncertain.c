#include <stdio.h>
#include <stdlib.h>

static void check_ptr(void *p) {
    if (p == NULL) {
        fprintf(stderr, "bellek yok\n");
        exit(1);
    }
}

int *helper_after_use(int n) {
    int *v = malloc(n * sizeof(int));
    v[0] = n;
    check_ptr(v);
    return v;
}

int *through_alias(int n) {
    int *a = malloc(n * sizeof(int));
    int *b = a;
    if (!b) return NULL;
    a[0] = n;
    return a;
}
