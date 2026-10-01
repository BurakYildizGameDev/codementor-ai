#include <stdio.h>

int main(void) {
    int n, x, sum = 0;
    if (scanf("%d", &n) != 1) return 1;
    while (scanf("%d", &x) == 1) sum += x;
    int read = scanf("%d", &x);
    if (read != 1) return 2;
    printf("%d\n", sum);
    return 0;
}
