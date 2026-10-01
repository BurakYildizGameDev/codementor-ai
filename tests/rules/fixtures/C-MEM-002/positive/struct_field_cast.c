// EXPECT: 9
#include <stdlib.h>

struct Stack { int *items; int size; int cap; };

void push(struct Stack *s, int v) {
    if (s->size == s->cap) {
        s->cap = s->cap ? s->cap * 2 : 4;
        s->items = (int *)realloc(s->items, s->cap * sizeof(int));
    }
    s->items[s->size++] = v;
}
