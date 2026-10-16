#include <stdio.h>

int main(void) {
    char buf[8];
    int value = 0;
    scanf("%7s", buf);
    scanf("%2d", &value);
    fscanf(stdin, "%99s", buf);
    fgets(buf, sizeof buf, stdin);
    return 0;
}
