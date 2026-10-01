// EXPECT: 7
#include <stdio.h>

int sum_file(FILE *f, int n) {
    int total = 0, x;
    for (int i = 0; i < n; i++) {
        fscanf(f, "%d", &x);
        total += x;
    }
    return total;
}
