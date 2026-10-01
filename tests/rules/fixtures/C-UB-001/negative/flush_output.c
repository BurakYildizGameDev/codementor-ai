#include <stdio.h>

int main(void) {
    printf("Ad: ");
    fflush(stdout);
    fprintf(stderr, "uyari\n");
    fflush(stderr);
    fflush(NULL);
    return 0;
}
