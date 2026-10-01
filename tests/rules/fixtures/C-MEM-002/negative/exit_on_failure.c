#include <stdio.h>
#include <stdlib.h>

int *grow(int *p, size_t n) {
    p = realloc(p, n * sizeof(int));
    if (p == NULL) {
        perror("realloc");
        exit(1);
    }
    return p;
}
