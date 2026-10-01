#include <stdio.h>

int main(void) {
    int n = 0;
    /* scanf("%d", &n); eski satır */
    (void)scanf("%d", &n);
    printf("scanf(\"%%d\") ile okundu: %d\n", n);
    return 0;
}
