#include <stdlib.h>

struct Buf { char *data; size_t cap; };

int resize(struct Buf *b, size_t cap) {
    char *bigger;
    bigger = (char *)realloc(b->data, cap);
    if (!bigger) return 0;
    b->data = bigger;
    b->cap = cap;
    return 1;
}
