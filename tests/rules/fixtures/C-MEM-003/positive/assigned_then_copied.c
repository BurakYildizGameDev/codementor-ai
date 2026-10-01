// EXPECT: 9, 11
#include <stdlib.h>
#include <string.h>

struct Person { char *name; };

void set_name(struct Person *p, const char *name) {
    char *copy;
    copy = calloc(strlen(name) + 1, 1);
    strcpy(copy, name);
    p->name = malloc(8);
    *p->name = '\0';
    free(copy);
}
