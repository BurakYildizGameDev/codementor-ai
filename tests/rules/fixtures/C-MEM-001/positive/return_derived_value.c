// EXPECT: 5, 11
#include <stdlib.h>

int first(void) {
    int *p = malloc(4 * sizeof(int));
    p[0] = 7;
    return p[0];
}

int try_alloc(int n) {
    char *buf = malloc(n);
    return buf != NULL;
}
