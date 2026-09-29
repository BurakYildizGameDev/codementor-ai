// EXPECT: 6
#include <stdio.h>

int main(void) {
    char name[16];
    gets(name);
    printf("%s\n", name);
    return 0;
}
