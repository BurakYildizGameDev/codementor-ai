#include <stdlib.h>

int pair(void) {
    int *a = malloc(4);
    int *b = malloc(4);
    if (a == NULL) {
        return 1;
    } else if (b == NULL) {
        free(a);
        return 1;
    }
    a[0] = b[0];
    free(b);
    free(a);
    return 0;
}

int validated(int n) {
    int *p = malloc(4);
    if (n < 0) return 2;
    else if (!p) return 1;
    p[0] = n;
    free(p);
    return 0;
}

int labeled(void) {
    int *p = malloc(4);
check:
    if (p == NULL) return 1;
    p[0] = 1;
    free(p);
    return 0;
}

int *retry(void) {
    int *p;
    while (1) {
        p = malloc(4);
        if (p) break;
    }
    p[0] = 1;
    return p;
}
