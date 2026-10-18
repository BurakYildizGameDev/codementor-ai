// EXPECT: 6
#include <stdlib.h>

void fill(int n) {
    int *p = NULL;
    if (p == NULL) p = malloc(n * sizeof *p);
    p[0] = n;
}
