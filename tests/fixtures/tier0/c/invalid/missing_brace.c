#include <stdio.h>

int square(int x) {
    return x * x;
}

int main(void) {
    for (int i = 0; i < 3; ++i) {
        printf("%d\n", square(i));
    }
    return 0; // expect-error
