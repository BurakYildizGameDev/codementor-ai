#include <stdlib.h>

struct Box { int *data; };

void keep(struct Box *box, int *data) {
    box->data = data;
}

void fill(struct Box *box, int n) {
    int *data = malloc(n * sizeof *data);
    keep(box, data);
}
