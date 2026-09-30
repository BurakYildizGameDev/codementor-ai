#include <stdio.h>

int max_of(const int *a, int n) {
    int best = a[0];
    for (int i = 1; i < n; i++) {
        if (a[i] > best) {
            best = a[i];
        }
    return best;
}
