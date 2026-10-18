// EXPECT: 5
#include <stdlib.h>

int first(int mode, int n) {
    int *p = malloc(n * sizeof *p);
    switch (mode) {
        case 0:
            if (p == NULL) return -1;
            break;
        default:
            break;
    }
    return p[0];
}
