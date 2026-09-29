// EXPECT: 5
#include <stdlib.h>

int sum(int n) {
    int *a = malloc(n * sizeof(int));
    int s = 0;
    for (int i = 0; i < n; i++) { a[i] = i; s += a[i]; }
    return s;
}
