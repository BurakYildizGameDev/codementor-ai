// EXPECT: 7
#include <stdio.h>
#include <stdlib.h>

int read_values(int n) {
    int *buf;
    if ((buf = malloc(n * sizeof *buf)) == NULL) return -1;
    for (int i = 0; i < n; i++) scanf("%d", &buf[i]);
    printf("%d\n", buf[0]);
    return 0;
}
