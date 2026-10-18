// EXPECT: 5
#include <stdlib.h>

int any_positive(int n) {
    int *p = malloc(n * sizeof *p);
    if (p[0] > 0) return 1;
    return 0;
}
