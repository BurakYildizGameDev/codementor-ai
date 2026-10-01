// EXPECT: 5
#include <stdlib.h>

int *zeros(int n) {
    int *a = malloc(n * sizeof(int));
    for (int i = 0; i < n; i++) a[i] = 0;
    return a;
}
