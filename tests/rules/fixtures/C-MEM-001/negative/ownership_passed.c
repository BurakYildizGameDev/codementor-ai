#include <stdlib.h>

struct List;
void list_add(struct List *list, char *item);

void add_item(struct List *list, int size) {
    char *item = malloc(size);
    list_add(list, item);
}
