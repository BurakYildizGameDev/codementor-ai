// EXPECT: 14
#include <stdlib.h>
#include <stdio.h>

void dump(const int *values, int n) {
    for (int i = 0; i < n; i++) printf("%d", values[i]);
}

void show(const int *values, int n) {
    dump(values, n);
}

int average(int n) {
    int *values = malloc(n * sizeof *values);
    if (values == NULL) return 0;
    for (int i = 0; i < n; i++) values[i] = i;
    show(values, n);
    return values[0];
}
