// EXPECT: 6
#include <stdlib.h>

char *grow(char *buf, size_t *cap) {
    *cap *= 2;
    buf = realloc(buf, *cap);
    if (buf == NULL) return NULL;
    return buf;
}
