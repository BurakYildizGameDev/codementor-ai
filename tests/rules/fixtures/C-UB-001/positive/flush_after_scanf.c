// EXPECT: 8
#include <stdio.h>

int main(void) {
    char c;
    int n;
    if (scanf("%d", &n) != 1) return 1;
    fflush(stdin);
    c = getchar();
    printf("%c\n", c);
    return 0;
}
