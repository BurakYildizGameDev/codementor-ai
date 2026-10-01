#include <stdlib.h>

int *grow(int *p, size_t n) {
    int *tmp = realloc(p, n * sizeof(int));
    if (tmp == NULL) {
        free(p);
        return NULL;
    }
    p = tmp;
    return p;
}
