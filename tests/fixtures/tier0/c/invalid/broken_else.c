#include <stdio.h>

int sign(int x) {
    if (x > 0) {
        return 1;
    } else if {  // expect-error
        return -1;
    }
    return 0;
}

int main(void) {
    printf("%d\n", sign(-5));
    return 0;
}
