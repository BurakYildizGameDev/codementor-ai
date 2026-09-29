#include <stdio.h>

struct point {
    int x;
    int y;
};

int main(void) {
    struct point p = { 1, 2 };
    int = p.x + p.y; // expect-error
    printf("%d\n", p.x);
    return 0;
}
