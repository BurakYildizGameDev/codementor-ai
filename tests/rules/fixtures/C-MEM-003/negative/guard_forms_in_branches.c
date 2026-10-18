#include <stdlib.h>

void same_case(int mode, int n) {
    int *p = malloc(n * sizeof *p);
    switch (mode) {
        case 0:
            if (p == NULL) return;
            p[0] = n;
            break;
        default:
            break;
    }
}

void once(int n) {
    int *p = malloc(n * sizeof *p);
    do {
        if (p == NULL) break;
        p[0] = n;
    } while (0);
}

void looped(int n) {
    int *p = malloc(n * sizeof *p);
    for (int i = 0; i < n; i++) {
        if (p == NULL) continue;
        p[0] = i;
    }
}

void reversed(int n) {
    int *p = malloc(n * sizeof *p);
    if (NULL == p) return;
    p[0] = n;
}
