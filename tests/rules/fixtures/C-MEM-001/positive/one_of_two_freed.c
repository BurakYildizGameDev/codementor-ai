// EXPECT: 6
#include <stdlib.h>
#include <string.h>

void copy_twice(const char *s, size_t n) {
    char *first = (char *)calloc(n + 1, 1);
    char *second = malloc(n + 1);
    memcpy(first, s, n);
    memcpy(second, s, n);
    free(second);
}
