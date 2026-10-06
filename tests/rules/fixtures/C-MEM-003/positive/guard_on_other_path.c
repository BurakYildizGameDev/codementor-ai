// EXPECT: 6, 18
#include <stdio.h>
#include <stdlib.h>

int *make(int n, int verbose) {
    int *a = malloc(n * sizeof(int));
    if (verbose) {
        if (a == NULL) {
            puts("bellek yok");
            return NULL;
        }
    }
    a[0] = n;
    return a;
}

char *lazy(char *buf) {
    if (buf == NULL) buf = malloc(64);
    buf[0] = '\0';
    return buf;
}
