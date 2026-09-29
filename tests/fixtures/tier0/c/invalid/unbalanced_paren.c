#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int *p = malloc(4 * sizeof(int));
    if ((p == NULL) { // expect-error
        return 1;
    }
    free(p);
    return 0;
}
