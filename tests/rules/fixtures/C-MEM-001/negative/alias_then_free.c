#include <stdlib.h>

struct Buf { char *data; int size; };

void scratch(void) {
    char *p = malloc(8);
    char *q;
    q = p;
    free(q);
}

struct Buf make_buf(int n) {
    char *p = malloc(n);
    struct Buf b = { p, n };
    return b;
}
